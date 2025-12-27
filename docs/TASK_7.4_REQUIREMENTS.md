# Task 7.4: Year Selector Requirements

## Working Examples to Reference
- Date Browser: src/ui/widgets/date_browser.py
- Browse Screen Integration: src/ui/screens/browse_screen.py (see show_date_browser method)

## ShowListWidget Interface
- load_shows(shows) - main method
- set_empty_state(message)
- set_loading_state()

## Database Query
- search_by_year(year) - returns list of show dicts

## Integration Pattern
1. Create year_browser.py widget
2. Add Year button to browse_screen left panel
3. Create show_year_browser() method (dialog pattern)
4. Create load_shows_by_year(year) handler
5. Connect signal: year_browser.year_selected.connect(handler)
