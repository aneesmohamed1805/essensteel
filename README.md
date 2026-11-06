# Essen Steel static review build

Status: In Review. The reference is the latest revised homepage board, “Steel strands and wire-drawing line.png”. The homepage retains the process strip visible in that board. It uses the supplied logo and outline symbol at their native aspect ratios. Photographic regions are extracted from the board as illustrative review assets. Replace them with rights-cleared full-resolution source files and have product geometry reviewed before launch.

## Run

From this directory, regenerate pages with `python3 build.py`. Serve `public/` with `python3 -m http.server --directory public 8000` and open http://localhost:8000/. The site has no application build dependencies. Exo loads from Google Fonts, with Arial as fallback.

## Environments

Pantheon development content reviewed: /products/, /about/, /technology/, /standards/, /sectors/, /sustainability/. Rendered dependencies identify WordPress, Blocksy, Blocksy Companion Pro, Stackable Premium, Contact Form 7 and Ultimate Addons for Contact Form 7. The static build does not depend on WordPress. The public homepage was checked for navigation and contact details.

GitHub: aneesmohamed1805/essensteel was empty at inspection. Cloudflare: Worker essensteel is connected to this repository and configured to deploy from the root with no build command and `npx wrangler deploy`. The production build targeted main and stopped while fetching the repository. The configuration in this package points Wrangler at the generated public/ directory. Establish a preview-only target before pushing, or approve a production deployment separately. Keep the preview robots.txt, HTML meta and X-Robots-Tag rules in place for review.

## Publication checks

- Keep /about/, /technology/, /standards/, /sectors/, /projects/ and /contact/ when reconciling the public URL inventory. /products/ and its six detail pages, /downloads/, /partnership/, /sustainability/ and /insights/ are included. Crawl existing deep links before cutover and map any retired URL to its closest replacement. Confirm sitewide canonicals and sitemap against the final domain.
- The contact and documentation CTAs use the sales address shown on Pantheon and the public website. They open the visitor’s email app. Connect and test a form endpoint if browser-based submission is required.
- Technical information is limited to product families and intended uses sourced from Pantheon. Match grades, dimensions, coating, packaging, strand construction and technical downloads to approved data sheets. Review the draft insights before publication.
- Obtain certificates with issuing body, scope and validity before adding ISO, product certification or authority approval claims. Review the board’s “Green Manufacturing” label and confirm evidence before publishing environmental benefits. Capacity, export destinations, project names, leadership and performance guarantees require separate evidence and approval. Review privacy and cookie copy against the final services.

The Git-backed review project is `essensteel-git-review` on Cloudflare Pages. It builds from `review` and serves the `public/` directory without a build command. Review URL: https://essensteel-git-review.pages.dev/.
