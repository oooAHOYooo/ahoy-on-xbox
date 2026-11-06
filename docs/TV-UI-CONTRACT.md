# Ahoy TV shared UI contract

This contract defines the screen structure and interaction model shared by the Xbox and Fire TV apps. Each platform uses its native UI toolkit and input APIs; the visible hierarchy, labels, selection behavior, and design tokens stay aligned.

## Shared shell

- Full-screen video or selected artwork is the background stage.
- The header places the Ahoy mark on the left, four section tabs in the center, and live/account status on the right.
- The program information block sits over the lower left of the background and shows channel context, title, secondary title/host, description, and the primary playback action.
- A bottom shelf shows the current section's selectable cards. Live TV uses channel cards; On Demand, Music, and Podcasts use media cards.
- Cards use artwork where available, a dark text gradient, readable metadata, and a clear pink selected/focused outline.

## Sections and labels

Use the same order and user-facing labels on both platforms:

1. `LIVE TV`
2. `ON DEMAND`
3. `MUSIC`
4. `PODCASTS`

Changing a section updates the selected tab, hero content, shelf contents, and playback context together. Live TV presents channels 101–104 in the shelf. Other sections present their media items using the same card pattern.

## Interaction semantics

The meaning of each action is shared even when the physical button differs:

| Action | Behavior |
| --- | --- |
| Navigate | Move focus between tabs and cards; focused cards update the hero selection. |
| Select | Start the focused item, or tune the focused channel. |
| Back / Guide | Return to the live guide or previous browse state; do not silently discard playback context. |
| Save | Toggle the focused item's saved state when the platform supports it. |
| Account | Open platform account pairing when that platform implements pairing. |
| Fullscreen | Expand playback and provide a clear way back to browsing. |

Xbox may map Save and Account to controller buttons and show its pairing overlay. Fire TV may omit those actions until its account service is implemented. This does not change the shared screen hierarchy or the meaning of navigation and selection.

## Visual tokens

| Token | Value | Use |
| --- | --- | --- |
| Background | `#000000` | Full-screen stage and shell |
| Accent | `#FF0060` | Selected tab, active state, focus outline, live emphasis |
| Card surface | `#141418` / `#1C1C22` | Shelves, cards, and controls |
| Primary text | `#FFFFFF` | Titles and selected labels |
| Secondary text | `#8E8E93` | Supporting details and inactive labels |
| Focus outline | `#FF0060` | Focused card or control |

Card corners are approximately 18dp on Fire TV and a proportional equivalent on Xbox. Controls use compact rounded rectangles (about 6dp corners), with solid pink for the selected tab and charcoal for inactive tabs.

## Platform implementation rule

Keep data, focus handling, playback, and platform accessibility native. Implementations should be reviewed against this contract rather than copying platform widgets across frameworks. When a platform cannot support an item or action, preserve the layout and hide or disable that action without changing the shared navigation model.
