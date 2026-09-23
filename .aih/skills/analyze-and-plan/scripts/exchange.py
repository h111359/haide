"""Deterministic Markdown questionnaires and reviewed plain-text exchanges."""
from __future__ import annotations
import re
from contracts import Error, digest, now, screen, uid, identifier

HEAD = re.compile(r"^## ([A-Za-z0-9_.-]+)\s*\|\s*revision=(\d+)\s*\|\s*respondent=(Framework user|Requestor)\s*\|\s*kind=(single|multiple|text)\s*\|\s*blocker=(true|false)\s*\|\s*category=(requirement|design)\s*$")
FIELDS = {"Question": "question", "Explanation": "explanation", "Why we ask": "why", "How to answer": "instructions", "Example": "example", "Default": "default", "Answer": "answer", "Comments": "comments"}


def render(questions, title="Clarification questionnaire"):
    lines = [f"# {title}", "", "Saved answers are drafts until an explicit Clarify or Analyze submission.", ""]
    for q in questions:
        lines += [f"## {q['id']} | revision={q.get('revision', 1)} | respondent={q.get('respondent', 'Framework user')} | kind={q.get('kind', 'text')} | blocker={str(q.get('blocker', True)).lower()} | category={q.get('category', 'requirement')}", ""]
        for label, key in FIELDS.items():
            if key in ("answer", "comments"):
                continue
            lines.append(f"{label}: {q.get(key, '')}")
        lines.append("")
        selected = q.get("selected", [])
        for option in q.get("options", []):
            lines.append(f"- [{'x' if option in selected else ' '}] {option}")
        lines += [f"Answer: {q.get('answer', '')}", f"Comments: {q.get('comments', '')}", ""]
    return "\n".join(lines) + "\n"


def parse_questionnaire(text):
    screen(text, "questionnaire")
    questions, q, active_field = [], None, None
    for line in text.splitlines():
        match = HEAD.match(line)
        if match:
            if q:
                questions.append(q)
            qid, revision, respondent, kind, blocker, category = match.groups()
            q = {"id": qid, "revision": int(revision), "respondent": respondent, "kind": kind, "blocker": blocker == "true", "category": category, "options": [], "selected": [], "answer": "", "comments": ""}
            active_field = None
        elif line.startswith("## "):
            raise Error("questionnaire-format", "Malformed question heading; retain the stable question ID and fields.")
        elif q is not None:
            choice = re.match(r"^- \[([ xX])\] (.+)$", line)
            if choice:
                q["options"].append(choice[2])
                if choice[1].lower() == "x":
                    q["selected"].append(choice[2])
                active_field = None
                continue
            found = False
            for label, key in FIELDS.items():
                if line.startswith(label + ":"):
                    q[key] = line[len(label) + 1:].strip()
                    active_field, found = key, True
                    break
            if not found and active_field and line.strip():
                q[active_field] += "\n" + line
    if q:
        questions.append(q)
    ids = [q["id"] for q in questions]
    if len(ids) != len(set(ids)):
        raise Error("duplicate-question", "Question IDs must be unique.")
    for q in questions:
        for field in ("question", "explanation", "why", "instructions"):
            if not q.get(field):
                raise Error("questionnaire-format", f"{q['id']} needs {field}.")
        if q["kind"] == "single" and len(q["selected"]) > 1:
            raise Error("conflicting-answer", f"{q['id']} permits one checked choice; reconcile the answer before submitting.")
        if q["kind"] != "text" and not q["options"]:
            raise Error("questionnaire-format", f"{q['id']} needs choices or kind=text.")
        if q["selected"] and q["answer"]:
            q["requires_semantic_review"] = True
    return questions


def answered(q):
    def meaningful(value):
        value = value.strip().casefold().replace("’", "'")
        unknown = ("i don't know", "i do not know", "needs discussion", "unknown")
        return bool(value) and not any(value == item or value.startswith(item + " /") for item in unknown)
    return meaningful(q.get("answer", "")) or any(meaningful(value) for value in q.get("selected", []))


def export_form(request, questions, interpretation_revision, previous=None):
    selected = [q for q in questions if q.get("respondent") == "Requestor" and not answered(q) and not q.get("withdrawn")]
    if not selected:
        return None
    signature = digest({"request": request["id"], "questions": selected, "interpretation_revision": interpretation_revision})
    if previous and previous.get("signature") == signature:
        return previous
    form_id = uid("FORM")
    lines = ["AIH — questions about your requested change", f"Request: {request['id']}", f"Form: {form_id}", "Form revision: 1", f"Generated: {now()}", f"Title: {request.get('title', 'Product change')}", "", request.get("summary", request.get("title", "")), "", "Please keep the Request, Form and question references. Open this file in any text editor.", "Mark [x] for choices, or write after Answer:. Use Comments: for an alternative or extra information.", "You may leave a question unanswered or write I don't know / Needs discussion. Return the completed file to the framework user.", "These answers describe your needs; they cannot approve a plan or start implementation.", ""]
    for q in selected:
        lines += [f"## {q['id']} | revision={q['revision']} | respondent=Requestor | kind={q['kind']} | blocker={str(q['blocker']).lower()} | category={q.get('category', 'requirement')}", f"Question: {q['question']}", f"Explanation: {q['explanation']}", f"Why we ask: {q['why']}", f"How to answer: {q['instructions']}", "Essential answer" if q["blocker"] else f"Optional; default if unanswered: {q.get('default', 'remain unknown')}"]
        if q.get("example"):
            lines.append("Example: " + q["example"] + " (illustration only, not a prefilled answer)")
        lines += [f"- [ ] {option}" for option in q.get("options", [])]
        lines += ["Answer: ", "Comments: ", ""]
    text = "\n".join(lines)
    return {"schema_version": "1.0", "id": form_id, "request_id": request["id"], "revision": 1, "created": now(), "interpretation_revision": interpretation_revision, "signature": signature, "questions": selected, "text": text, "sha256": digest(text)}


def receive(text, current_request, forms, current_questions, review_revision):
    screen(text, "returned answers")
    form_matches = re.findall(r"^Form:\s*(\S+)\s*$", text, re.M)
    request_matches = re.findall(r"^Request:\s*(\S+)\s*$", text, re.M)
    form_id = form_matches[0] if len(form_matches) == 1 else None
    request_id = request_matches[0] if len(request_matches) == 1 else None
    form = next((f for f in forms if f["id"] == form_id), None)
    rows, recognized, seen = [], [], set()
    chunks = re.split(r"(?=^## )", text, flags=re.M)
    for chunk in chunks:
        if not chunk.startswith("## "):
            continue
        try:
            qs = parse_questionnaire(chunk)
        except Error:
            rows.append({"question_id": None, "status": "malformed", "original": chunk, "answer": ""})
            continue
        for q in qs:
            qid = q["id"]
            old = next((item for item in (form or {}).get("questions", []) if item["id"] == qid), None)
            current = next((item for item in current_questions if item["id"] == qid), None)
            status = "matched"
            if request_id != current_request or form is None:
                status = "unassigned"
            elif qid in seen:
                status = "duplicate"
            elif old is None:
                status = "unknown"
            elif current is None or current.get("withdrawn"):
                status = "withdrawn"
            elif old["revision"] != q["revision"] or current["revision"] != q["revision"]:
                status = "stale"
            elif old["question"] != q["question"] or old.get("options", []) != q.get("options", []):
                status = "altered"
            elif not answered(q):
                status = "unanswered"
            elif answered(current) and (current.get("answer") != q.get("answer") or current.get("selected") != q.get("selected")):
                status = "conflict"
            seen.add(qid)
            rows.append({"question_id": qid, "question_revision": q["revision"], "question": (old or q)["question"], "explanation": (old or q).get("explanation"), "previous_answer": (current or {}).get("answer", ""), "answer": q["answer"], "selected": q["selected"], "comments": q["comments"], "status": status, "attributed_to": "Requestor"})
            recognized.append(qid)
    duplicates = {qid for qid in recognized if recognized.count(qid) > 1}
    for row in rows:
        if row.get("question_id") in duplicates:
            row["status"] = "duplicate"
    for old in (form or {}).get("questions", []):
        if old["id"] not in recognized:
            rows.append({"question_id": old["id"], "status": "missing", "question": old["question"], "answer": ""})
    return {"schema_version": "1.0", "id": uid("RECEIPT"), "created": now(), "request_id": request_id, "form_id": form_id, "sha256": digest(text), "text": text, "rows": rows, "review_revision": review_revision, "status": "staged" if request_id == current_request and form else "unassigned", "outside_answer_text": text.split("## ", 1)[0], "reviewer": None}


def review(questions, receipt, decisions, revision):
    if receipt["review_revision"] != revision:
        raise Error("revision-conflict", "Input, amendments, questions or saved answers changed during review. Refresh and reconcile the review.", {"expected": receipt["review_revision"], "actual": revision})
    result = [dict(q) for q in questions]
    seen = set()
    for decision in decisions:
        qid = decision.get("question_id")
        if qid in seen:
            raise Error("duplicate-review", "Review each question once.")
        seen.add(qid)
        q = next((q for q in result if q["id"] == qid), None)
        row = next((r for r in receipt["rows"] if r.get("question_id") == decision.get("source_question_id", qid)), None)
        choice = decision.get("choice", "unresolved")
        if choice in ("retain", "unresolved"):
            continue
        if choice not in ("accept", "edit") or q is None:
            raise Error("review-mapping", "Explicitly match the answer to a current question and select accept, edit, retain or unresolved.")
        if row is None and choice != "edit":
            raise Error("review-mapping", "The received answer needs an explicit manual correction/matching record.")
        if row and row["status"] not in ("matched", "conflict", "unanswered") and not decision.get("resolve_conflict"):
            raise Error("review-conflict", f"Resolve {row['status']} answer for {qid} explicitly.")
        if choice == "accept" and any(field in decision and decision[field] != (row or {}).get(field, [] if field == "selected" else "") for field in ("answer", "selected", "comments")):
            raise Error("review-attribution", "Changed wording or choices require Edit so the correction is attributed to the framework user.")
        answer = decision.get("answer", (row or {}).get("answer", ""))
        screen(answer, "review correction")
        q["answer"] = answer
        q["selected"] = decision.get("selected", (row or {}).get("selected", []))
        if any(x not in q.get("options", []) for x in q["selected"]):
            raise Error("review-choice", "Selected answer is not a current option.")
        q["comments"] = screen(decision.get("comments", (row or {}).get("comments", "")), "review comments")
        q["source"] = {"receipt_id": receipt["id"], "attributed_to": "Framework user correction" if choice == "edit" else "Requestor", "submitted_by": "Framework user"}
    parse_questionnaire(render(result))
    return result
