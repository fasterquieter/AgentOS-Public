# TrailCache product definition

Verified: 2026-08-20 from accepted product brief and vocabulary review.

## Purpose

TrailCache lets hikers capture a private journal entry with notes, location, and photos without network access, then back it up and converge across their devices when connectivity returns.

## Vocabulary

- **Entry:** one journal record for a hike or observation. Never call it a Post.
- **Trail:** optional named route associated with an Entry. A Place is not a Trail.
- **Journal:** the user's ordered collection of Entries on the device.
- **Backup:** cloud persistence of an Entry; not proof that local content may be discarded.

## Current platforms

iOS and Android share domain and sync logic. UI is platform-native. The cloud service stores encrypted user payloads and photo objects.

## Non-goals

Public social posting, collaborative editing, real-time tracking, and server-authoritative content moderation are outside current scope.

