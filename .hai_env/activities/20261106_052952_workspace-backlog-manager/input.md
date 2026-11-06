I need new agent in hai_agents_library which to manage a backlog for the workspace. The backlog should be recorded in a folder which could be located anywhere in the workspace, not necessary under .hai_env/ . In this folder should have subfolders `new` and `closed` and in them should be positioned the backlog items which are pending to be realized and the completed/cancelled/rejected respectively. Each backlog item should be in a separate file. In the backlog folder should be kept a cataloue of backlog items. Some draft for baclog items are written here - backlog/new\.md. Transform those to backlog items in the new structure. The new agent should take care for all these.

User follow-up: Remove this dependency and remove imports folder. The original file can be moved in the current activity to be preserved for audit purposes but it should not be reffered


User acceptance of BL-0006 completion recommendation: ok - proceed
