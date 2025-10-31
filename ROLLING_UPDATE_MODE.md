# Rolling Update Mode

## Overview
New posting mode that updates the same Reddit post for N days before creating a new one.

## Configuration

Add to `config.toml`:

```toml
[reddit]
postMode = "rolling_update"  # New mode

[reddit.rolling]
days_before_new_post = 7  # Create new post after 7 days
update_existing = true     # Update the existing post
```

## How It Works

1. **First Release**: Creates a new Reddit post
2. **Subsequent Releases (Days 0-6)**: Updates the existing post with new changes
3. **Day 7+**: Creates a new post and starts the cycle again

## Behavior

### When Post Age < 7 Days:
- Edits the existing post body
- Accumulates all changes in one post
- Updates `last_posted_versions` in state
- No new post created

### When Post Age >= 7 Days:
- Creates a new post
- Marks old post as outdated (if configured)
- Resets the 7-day cycle

## Example Timeline

```
Day 0: New post created "BitLife v1.0"
Day 2: Post updated "BitLife v1.0, BitLife Go v2.0"
Day 4: Post updated "BitLife v1.0, BitLife Go v2.0, BitLife v1.1"
Day 7: New post created "BitLife v1.1, BitLife Go v2.0"
```

## Modes Comparison

| Mode | Behavior |
|------|----------|
| `direct_link` | New post for every release |
| `landing_page` | New post for every release (with landing page) |
| `rolling_update` | Update same post for N days |

## State Management

The bot tracks:
- `activePostId`: Current post being updated
- `last_posted_versions`: Versions in current post
- Post creation timestamp (from Reddit API)

## Benefits

- Reduces post spam
- Consolidates updates
- Easier for users to follow
- Configurable update window
