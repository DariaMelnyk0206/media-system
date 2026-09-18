# Conflict Resolution Record

## Conflict

A merge conflict occurred in `spec/idea.md` between a human change and a coding-agent change.

The human change stated that each media item should belong to one primary topic, while a topic could contain multiple media items.

The coding-agent change clarified the relationship as many-to-many: one topic can contain multiple media items, and one media item can belong to multiple user-defined topics.

## Resolution

The many-to-many version was retained.

The decision was based on the content of the existing project idea, not on who created the change or which change was made later. The initial description already stated that the same media item can belong to multiple topics and that the relationship should work in both directions.

## Lab 2 Question

No new unresolved requirement was identified as a result of this conflict. The relationship between media items and topics was sufficiently defined by the initial project idea for this case.
