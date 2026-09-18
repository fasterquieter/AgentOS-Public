# Screen-reader journal navigator

Status: active
Reviewed: 2026-07-30

## Use context

Experienced mobile screen-reader user navigating by headings and controls. Has 1,200 Entries and relies on search/filter state being announced.

## Goals

Find a prior Entry, understand active filters, add a captioned photo, and recover from upload failure without switching input mode.

## Behaviors and mental model

Expects filter chips to expose selected state and result count changes to be announced without moving focus. Uses control labels rather than visual proximity to infer which photo an action affects.

## Evidence basis

Synthetic persona reviewed against platform accessibility guidance. No direct TrailCache user research yet; conclusions require accessibility testing, not persona authority.

## Scenarios

1. Navigate journal headings and filters with screen reader enabled; select/clear a Trail filter.
2. Attach three photos, distinguish their remove/retry controls, and add captions.
3. Recover from an expired upload session while the local Entry remains readable.

