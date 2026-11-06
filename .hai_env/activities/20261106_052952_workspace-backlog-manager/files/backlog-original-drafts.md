## 20261029_0554 Agents chat

### What

In the current activity to be imitated a chat between the agents summon to act on this activity

### Why

Agents to be able to communicate between each other if need to leave messages for future work related information other agents will benefit from.

### Acceptance Criteria

All agents summon for the activity can read and write to the chat
Agent can not delete a message in the chat already posted
The chat is specific for the activity - new activity will have a separate chat



## 20261029_0555 Usage records

### What

In the current activity folder to be added a markdown file with the usage and spend details. In it, similar to the chronicles update, should be updated the spent tokens and the used credits and the money equivalent.

### Why

The user should be able to track the usage

### Acceptance Criteria

When asked bu the user, the usage is updated with the spent from the sessions related to this activity
Before the activity is closed - the usage should be updated


## 20261029_0809 Initial Menu and Help

### What

The leader during execution of start should guide the user what are the possible commands which are available currently. Also, HAI will not have specific user guide, but education of the user should happen via communication with the leader.

### Why

I don't want to maintain static user guides, helps and instructions. But I want to have the feeling of communication with a real person who can explain to me what can I do and how should I do it. In the same course of thoughts, I want to avoid the need to provide a menu to the user, but this conversation actually to be the menu, via which the user can choose the next actions. So the menu is something which provides the possible options and the ability the user to select specific option.

### Acceptance Criteria

On start, the leader explains shortly and in nice-looking way what the user currently can do. For example, can create new activity, or can close the current activity, or can proceed with analysis of requirements, or something like that. Also, the leader should propose to explain or to generate help materials to the user, which could be temporary and stored in the activity, or they could be permanently stored in the workspace, depending on the preferences of the user.


## 20261029_0816 Better Instructions

### What

The instructions in skills or concepts should be clearly written in a simple language, which is understandable for everyone, especially for non-specialists, and in a way that ambiguity is avoided. When a term is used, it should be defined. The text should clearly identify for what scope and for what element it is related and should not assume that the reader will understand the intention which generate this text. 

### Why

The definitions of agent should be easily verifiable and further changes on the agent should not confuse or add a narrative which cannot be understood and cannot be verified.


## 20261029 Agents Collection

### What

I want to keep the HAI-specific agents to the minimum and to be able to extend the workspaces where HAI is installed with agents from a separate collection.

There should be still some principles and specific conventions which those agents in this collection should be consistent to, but  these agents should be independent from HAI. The agent defined in this colltheyection should be able to be executed as standalone. My current idea is when the agent is added to a workspace, there to be a specific mechanism establishing contract between the HAI framework and this agent. This contract mechanism actually should be something like a real contract between an expert and a company, in which contract is defined the specifics for this expert to work in this company, without defining the expert knowledge and expert skills itself. For example, in this contract should be defined how the expert will receive the needed information for its work, like where to generate the output or from which files to read its input. And by default this agent either should be instructed explicitly, or should ask for these parameters. So when it is executed as standalone, it will take care to understand the proper input information needed and the proper output destinations required.


## 20261029_0832 Project Manager and Backlog

### What

To be created a new agent with purpose project manager or scrum master, who is taking care about the backlog. The backlog is currently in a separate folder where it is supposed to have a file new.mdm where the new user stories are written. This new agent project manager should take care to take a specific user story and to form from it input in the current activity and to move the user story to a new file, completed.md, in the backlog folder when the user story is implemented. Along with each user story definition in New.md and Completed.md, this project manager should add system information about this user story, status, time of completion, relation to the specific activity, where it is completed, etc.

### Acceptance Criteria

Each user story should follow a specific format, where the header contains the time, date and time for creation of the user story, followed by the title of the user story very shortly. Then three subheaders, headers level three, which are fixed. First header is named What, second header is named Why, and third header is named Acceptance Criteria.



## 20261029_0837

### What

The current agent advisor in .hai_env/ is scoped to very specific task, but the name Advisor is too generic. This agent should be renamed in a proper way, because I need other advisors as well to be created as additional agents.




## 20261029_0839

### What

I need additional agent to act as business analyst, which purpose will be to clarify the user story or change requests in the backlog. To clarify the backlog item, let's say in that way. From business perspective, and to transfer this backlog item in well-defined input in the current activity.



## 20261029_1856

### What

Every agent should be able to have a setup parameters when deployed in a specific workspace