---
name: clickup-tasks
description: >-
  Creates, assigns, prioritizes, and updates the status of ClickUp tasks via
  MCP. Use when the user explicitly asks to create a task, assign someone,
  change priority, or move a task's status.
---

# ClickUp tasks

## Steps
1. Identify the List (check `knowledge/_shared/clickup-map.md`; ask the user if ambiguous).
2. For creation: get task name, and optionally assignee, priority (Urgent/High/Normal/Low), due date, description.
3. For updates: find the task by name/ID via MCP search before modifying it — never guess a task ID.
4. Confirm the action taken (task name, list, assignee, priority, status) in your reply.
5. Never create, assign, reassign, or change the status/priority of a task unless the user explicitly asked for that action in this message.

## Statuses
Use the List's actual configured statuses (fetch via MCP) rather than assuming a fixed set — statuses vary per List/Space in ClickUp.
