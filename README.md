# Essen Steel static review build

Status: In Review. The reference is the latest revised homepage board, “Steel strands and wire-drawing line.png”. The homepage retains the process strip visible in that board. It uses the supplied logo and outline symbol at their native aspect ratios. Photographic regions are extracted from the board as illustrative review assets. Replace them with rights-cleared full-resolution source files and have product geometry reviewed before launch.

## Run

From this directory, regenerate pages with `python3 build.py`. Serve `public/` with `python3 -m http.server --directory public 8000` and open http://localhost:8000/. The site has no application build dependencies. Exo loads from Google Fonts, with Arial as fallback.

## Environments

Pantheon development content reviewed: /products/, /about/, /technology/, /standards/, /sectors/, /sustainability/. Rendered dependencies identify WordPress, Blocksy, Blocksy Companion Pro, Stackable Premium, Contact Form 7 and Ultimate Addons for Contact Form 7. The static build does not depend on WordPress. The public homepage was checked for navigation and contact details.

GitHub: aneesmohamed1805/essensteel was empty at inspection. Cloudflare: Worker essensteel is connected to this repository and configured to deploy from the root with no build command and `npx wrangler deploy`. The production build targeted main and stopped while fetching the repository. The configuration in this package points Wrangler at the generated public/ directory. Establish a preview-only target before pushing, or approve a production deployment separately. Keep the preview robots.txt, HTML meta and X-Robots-Tag rules in place for review.

## Publication checks

- Keep /about/, /technology/, /standards/, /sectors/, /projects/ and /contact/ when reconciling the public URL inventory. /products/ and its six detail pages, /downloads/, /partnership/, /sustainability/ and /insights/ are included. Crawl existing deep links before cutover and map any retired URL to its closest replacement. Confirm sitewide canonicals and sitemap against the final domain.
- The contact and documentation CTAs use the sales address shown on Pantheon and the public website. Connect and test the Mailgun-backed enquiry form before enabling browser-based submission.
- Technical information is limited to product families and intended uses sourced from Pantheon. Match grades, dimensions, coating, packaging, strand construction and technical downloads to approved data sheets. Review the draft insights before publication.
- Obtain certificates with issuing body, scope and validity before adding ISO, product certification or authority approval claims. Review the board’s “Green Manufacturing” label and confirm evidence before publishing environmental benefits. Capacity, export destinations, project names, leadership and performance guarantees require separate evidence and approval. Review privacy and cookie copy against the final services.

The Git-backed review project is `essensteel-git-review` on Cloudflare Pages. It builds from `review` and serves the `public/` directory without a build command. Review URL: https://essensteel-git-review.pages.dev/.

### Add an Insight

Add the article at the top of the `stories` list in `build.py`. The Insights index shows the full list and the homepage shows its first two entries. Add distinct `home-<slug>.webp` and `index-<slug>.webp` thumbnails under `public/assets/insights/`, and put the article image named in the story entry under `public/assets/`. Regenerate the static pages with `python3 build.py` and commit the source, assets and generated HTML together.

## Public-site migration review — 6 November 2026

Compared the public Home, About, Technology, Sectors, Standards, Projects and Contact pages with the Cloudflare review build. The existing top-level paths are retained. The new blocks cover Kizad logistics, inline and specialist production lines, in-house testing and document requests. The Applications page carries forward additional uses from the old Sectors page. The Contact page links to a map search for the published business name.

| Candidate wording or legacy item | Source and scope | Evidence and publication status |
| --- | --- | --- |
| “Inline E-Phos System”, “Low Relaxation Line”, “Aluminium Cladding Line”, “Stranding Line” and “Galva Green Technology” | https://www.essensteel.com/technology/ — manufacturing lines, reviewed 2026-11-06 | Descriptive review copy added. Confirm the current equipment inventory and available products with Essen before launch. |
| “chemical-free”, “zero impact on the environment”, “heat input levels to 30%” and “highest DV in the world” | https://www.essensteel.com/technology/ — legacy galvanising claims, reviewed 2026-11-06 | Held. Obtain a scoped process description and dated comparison, measurements or verification before publishing. |
| “79,200 MTPA”, “90,000 MTPA by end of 2021” and “564,000 Square Feet” | https://www.essensteel.com/about/ — capacity, target and site area, reviewed 2026-11-06 | Held. Corporate brochure gives a different capacity figure and target year. Confirm installed versus annual output capacity, current date and land versus built-up area. |
| “100% done in our world-class in-house testing facility”, “500 KN and 50 KN universal testing equipment” | https://www.essensteel.com/standards/ — laboratory coverage and equipment, reviewed 2026-11-06 | General testing description added for review. Hold coverage, ratings and equipment brand pending current lab scope and inventory. |
| ISO, DCL product conformity and UK CARES certificates | https://www.essensteel.com/standards/ — legacy certificate list, reviewed 2026-11-06 | Held pending current copies, issuer, product or facility scope, validity and client publication approval. |
| Company brochure, LRPC brochure and Quality, EHS and Energy policies | https://www.essensteel.com/about/, https://www.essensteel.com/sectors/ and https://www.essensteel.com/standards/ — linked legacy PDFs, reviewed 2026-11-06 | Request links are in review. Obtain current approved files for self-hosted downloads and decide redirects for the legacy PDF paths. |
| Riyadh City South Phase 1, Downtown Views 2 and Deira Mall | https://www.essensteel.com/projects/ — project names, reviewed 2026-11-06 | Held pending documented Essen supply role, project evidence and image permissions. Reconcile the three legacy detail URLs listed below before cutover. |
| Detailed standards, wire construction and product dimensions | https://www.essensteel.com/sectors/ and legacy LRPC brochure — product specifications, reviewed 2026-11-06 | Held pending approved data sheets and confirmation of current grades and standards. |
| Newsletter signup | Public footer, reviewed 2026-11-06 | Deferred pending an approved signup service, consent wording and recipient workflow. |

Legacy project URLs to reconcile during launch planning:

- `/portfolio_page/title-placeholder-for-third-project/` — Riyadh City South Phase 1
- `/portfolio_page/title-placeholder-for-second-project/` — Downtown Views 2
- `/portfolio_page/title-placeholder-for-first-project/` — Deira Mall

If approved detail pages are prepared, redirect each legacy path to its corresponding page. Otherwise, review each destination with the site owner before setting redirects.
