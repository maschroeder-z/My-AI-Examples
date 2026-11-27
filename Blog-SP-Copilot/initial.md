Create a modern, responsive, and interactive HTML application that presents the content of the underlying SharePoint list or library in a professional blog-style user interface.

The application should provide an intuitive way to discover, search, filter, and read published articles.

### 1. General layout

Create a clean, modern, and visually appealing interface consisting of three main areas:

- A full-width search and navigation area at the top.
- A filter panel on the left side, occupying approximately 25% of the available width.
- An article preview area on the right side, occupying approximately 75% of the available width.

Use a light background, rounded corners, subtle shadows, sufficient white space, and a professional typography style inspired by Microsoft Fluent UI.

### 2. Search area

Place a prominent search box at the top of the application.

- Display the placeholder text "Search articles...".
- Include a search icon and a button to clear the search text.
- Search across article titles, introduction texts, authors, and tags.
- Update the search results dynamically while the user is typing.
- Display the number of matching articles.

### 3. Left-side filter panel

Create a vertical filter panel with the heading "Filter articles".

Include the following filter options:

**Created by / Author**
- Dynamically retrieve all available authors from the underlying data source.
- Display authors as selectable checkboxes.
- Allow multiple authors to be selected.

**Tags / Keywords**
- Dynamically retrieve all available tags from the articles.
- Display tags as selectable badges or checkboxes.
- Display the number of associated articles next to each tag.
- Allow multiple tags to be selected.

**Publication time range**
- Provide predefined time ranges:
  - All time
  - Last 7 days
  - Last 30 days
  - Last 3 months
  - Last 12 months
- Additionally, provide a start-date and end-date picker to define a custom time range.

All filters must work in combination with the search functionality. Provide a "Clear all filters" button to reset the selection.

### 4. Article preview area

Display articles as visually appealing blog preview cards in a responsive grid layout.

Each article card must contain:

- A large preview or thumbnail image with a consistent 16:9 aspect ratio.
- The article title as a prominent, clickable heading.
- The author's name and profile picture, if available.
- The creation or publication date.
- Associated tags displayed as small, colored badges.
- The article introduction text, limited to approximately three or four lines.
- A "Read article" link or button that opens the original article in SharePoint.

If no preview image is available, display a neutral placeholder image.

Add a subtle hover effect to each article card to indicate that it is interactive.

### 5. Sorting and display options

Above the article preview area, provide:

- The total number of matching articles.
- A sorting dropdown with the options:
  - Newest first (default)
  - Oldest first
  - Title A–Z
  - Title Z–A
- A toggle to switch between grid view and compact list view.

Initially display 12 articles and provide a "Load more articles" button if additional articles are available.

### 6. Interactive behavior

Implement the following functionality:

- Real-time search without reloading the page.
- Dynamic filtering by author, tags, and publication date.
- Combined search and filter operations.
- Clickable article tags that automatically apply the corresponding tag filter.
- Active filters displayed above the article results as removable badges.
- A user-friendly message if no matching articles are found.
- A loading indicator while retrieving data.
- Appropriate error handling if the data cannot be retrieved.

### 7. Responsive design

Ensure that the application works on desktop computers, tablets, and mobile devices.

- Desktop: display the filter panel on the left and three article cards per row where space permits.
- Tablet: display two article cards per row.
- Mobile: display one article card per row and make the filter panel collapsible.

### 8. Data integration and technical requirements

- Use the actual data from the underlying SharePoint list or document library.
- Analyze the available columns and map them to the corresponding article properties, including title, author, creation date, tags, introduction text, preview image, and article URL.
- Do not use hardcoded sample articles.
- Handle missing or empty field values gracefully.
- Use HTML, CSS, JavaScript, and the libraries available within the SharePoint HTML application environment.
- Use the supported SharePoint data access mechanisms.
- Respect the permissions of the current SharePoint user.
- Make the application accessible, including keyboard navigation, accessible form labels, and alternative text for images.
- Generate a complete, functional HTML application, not just a static visual mockup.

The final result should look like a professional online magazine or corporate knowledge portal and provide a significantly improved user experience compared to a traditional SharePoint list view.