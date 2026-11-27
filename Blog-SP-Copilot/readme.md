# SharePoint Blog Experience – HTML Apps with Copilot

Transform a traditional SharePoint list or Site Pages library into a modern, interactive, and visually appealing blog experience using Microsoft Copilot and HTML-based applications in SharePoint.

This repository contains ready-to-use Copilot prompts that enable users to generate a professional blog interface and an integrated article reading experience without manually writing HTML, CSS, or JavaScript code.

## Overview

SharePoint provides powerful capabilities for storing, managing, and publishing content. However, traditional list and library views are not always the best option for discovering and consuming articles.

With HTML-based applications and Microsoft Copilot, it is possible to create customized user interfaces that provide a significantly improved user experience while using existing SharePoint content and metadata.

The solution combines two Copilot prompts to create a modern blog experience comparable to an online magazine, corporate knowledge portal, or internal news platform.

## Repository contents

| Prompt | Description |
|---|---|
| **Blog User Interface** | Generates a responsive blog interface with article previews, dynamic search, filtering, and sorting capabilities. |
| **Article Reader Overlay** | Extends the blog interface with an integrated article reader that opens SharePoint content pages in an overlay without leaving the application. |

Both prompts can be used sequentially to build and extend the application with Microsoft Copilot.

## Features

### Modern blog interface

- Responsive and visually appealing article preview cards.
- Professional design inspired by Microsoft Fluent UI.
- Article thumbnail and preview images.
- Article titles and introduction texts.
- Author names and profile pictures.
- Creation and publication dates.
- Interactive keyword and tag badges.
- Grid and compact list views.
- Dynamic loading of additional articles.

### Interactive search

- Prominent search box at the top of the application.
- Real-time search across article metadata.
- Search by title, introduction text, author, and keywords.
- Dynamic display of matching article counts.
- Combined search and filter functionality.

### Dynamic filter panel

A dedicated filter panel allows users to discover relevant content based on different criteria:

- Created by / Author
- Tags and keywords
- Predefined publication time ranges
- Custom start and end dates
- Multiple filter selections
- Removable active filters
- Reset all filters

Filter options are dynamically generated from the underlying SharePoint data.

### Sorting

Articles can be sorted using the following options:

- Newest first
- Oldest first
- Title A–Z
- Title Z–A

### Integrated article reader

Instead of navigating away from the blog interface, users can open an article directly in an overlay by clicking its title, preview image, or "Read article" button.

The article reader provides:

- Large, responsive content overlay.
- Fixed article header.
- Article title, author, and publication date.
- Scrollable article content.
- Support for images and formatted content.
- Option to open the original SharePoint page.
- Multiple options to close the overlay.
- Full-screen reading experience on mobile devices.
- Preservation of the current search, filters, sorting, and scrolling position.

The objective is to create a seamless reading experience without interrupting the user's content discovery process.

## Application layout

The generated HTML application is organized into four main areas:

1. **Search area:** Full-width search functionality at the top.
2. **Filter panel:** Author, keyword, and publication date filters on the left.
3. **Article preview area:** Responsive article cards on the right.
4. **Article reader overlay:** Integrated reading experience displayed on demand.

## Recommended SharePoint data structure

The HTML application uses the existing content and metadata of the underlying SharePoint list or library.

The following columns are recommended:

| Column | SharePoint column type | Purpose |
|---|---|---|
| Title | Single line of text | Article title |
| Introduction | Multiple lines of text | Article introduction or summary |
| Thumbnail | Image | Article preview image |
| Author | Person or Group | Article author |
| Tags | Managed Metadata or Choice | Article classification |
| Created | Date and Time | Article creation date |
| Published | Date and Time | Article publication date |
| ArticleUrl | Hyperlink | URL of the original content page |

When using a SharePoint Site Pages library, existing system columns and metadata should be reused wherever possible.

The Copilot prompt instructs Copilot to analyze the available data structure and map the existing columns to the corresponding application properties.

## Getting started

### Step 1 – Prepare your SharePoint content

Create or select an existing SharePoint list or Site Pages library containing the articles you want to present.

Ensure that the required metadata, preview images, introduction texts, and article URLs are available.

### Step 2 – Generate the blog interface

1. Open the corresponding SharePoint environment.
2. Start the Copilot experience for creating HTML applications.
3. Open the **Blog User Interface** prompt from this repository.
4. Copy the complete prompt into Copilot.
5. Let Copilot generate the HTML application.
6. Preview the generated application and verify the data integration.
7. Refine the application using additional natural-language instructions if required.

### Step 3 – Extend the application with the article reader

1. Continue working with the previously generated HTML application.
2. Open the **Article Reader Overlay** prompt from this repository.
3. Copy the prompt into Copilot.
4. Instruct Copilot to extend the existing application.
5. Verify that clicking an article title opens the corresponding content page in the overlay.
6. Test the closing behavior and ensure that the previous search and filter settings are preserved.

### Step 4 – Publish and use the application

After validating the functionality and design, save and publish the generated HTML application using the capabilities available in your SharePoint environment.

## Prerequisites

- Access to SharePoint Online.
- Access to the Copilot functionality for creating and editing HTML applications in SharePoint.
- A supported SharePoint list or library containing article content.
- Appropriate permissions to access the underlying content.
- Availability of the required article metadata.

Feature availability may depend on Microsoft 365 licensing, tenant configuration, and the feature rollout status.

## Technical considerations

The prompts instruct Copilot to generate a complete and functional application based on the technologies and capabilities supported by the SharePoint HTML application environment.

The generated application should:

- Use supported HTML, CSS, and JavaScript capabilities.
- Retrieve actual SharePoint content instead of hardcoded sample data.
- Respect the permissions of the current SharePoint user.
- Handle missing metadata and preview images gracefully.
- Provide loading, empty-result, and error states.
- Support responsive layouts and accessible keyboard navigation.
- Avoid unsupported external dependencies.

Embedding complete SharePoint content pages in an overlay may be restricted by browser security policies or the SharePoint HTML application sandbox.

If direct embedding is not supported, the application should attempt to retrieve and safely render the supported article content. Opening the original SharePoint page in a separate browser tab should remain available as a fallback.

## Extend the solution with AI-powered content automation

The blog application can also be combined with an automated content assistant using Microsoft Copilot and Power Automate.

Such a workflow could automatically:

- Analyze newly created articles.
- Generate introduction texts and summaries.
- Identify relevant keywords.
- Assign tags to SharePoint content.
- Find and assign suitable article preview images.
- Maintain centralized tagging statistics.

The automated workflow enriches the SharePoint content and metadata, while the HTML application provides an optimized presentation and discovery experience.

Together, these capabilities enable an intelligent, AI-supported content publishing platform directly within SharePoint.

## Possible use cases

- Corporate blogs
- Internal news portals
- Knowledge management platforms
- Company intranets
- Technical documentation portals
- Project communication platforms
- Employee communication hubs
- Learning and training portals
- Product information portals
- Frequently asked questions and knowledge bases

## Benefits

| Benefit | Description |
|---|---|
| Low-code / No-code | Generate the application using natural-language prompts. |
| Rapid implementation | Create and refine customized interfaces with Copilot. |
| Improved user experience | Replace traditional list views with intuitive content discovery. |
| Integrated experience | Access and read articles without leaving the blog interface. |
| Reusability | Adapt the prompts to different SharePoint sites and content structures. |
| Existing data integration | Reuse SharePoint content, metadata, and permissions. |
| Extensibility | Extend the generated application with additional Copilot prompts. |
| Responsive design | Provide an optimized experience across different devices. |

## Important notes

This repository provides Copilot prompts rather than a precompiled or standalone HTML application.

The generated implementation may vary depending on the available SharePoint features, underlying data structure, Copilot responses, and tenant configuration.

Always review and test the generated application before using it in a production environment.

## Author

**Marc André Schröder-Zhou**

Microsoft MVP | Microsoft Certified Trainer | Independent Microsoft 365, SharePoint, Power Platform and AI Consultant

- Website: [www.dev-sky.net](https://www.dev-sky.net/)
- Technical Blog: [dev-sky.blog](https://dev-sky.blog/)
- YouTube: [@ZhouDevSky](https://www.youtube.com/@ZhouDevSky)

## Feedback and contributions

Feedback, suggestions, improvements, and additional use cases are welcome.

---

**From traditional SharePoint lists to modern content experiences – powered by Copilot!**

*Create. Customize. Discover. Read. All directly within SharePoint.*
