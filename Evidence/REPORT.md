# p2-20-symfony-demo — GREEN
Migration: **Symfony 6.4.47 → 7.4.0**.
Why meaningful: Symfony 6 to 7 removes deprecated framework/security/validator APIs and requires PHP >=8.2; full blog, authenticated comments/admin, forms and CLI suite retained.
Source: https://github.com/symfony/demo @ 72040e73b3deed4281706bb5dda1ff1321f00396.
Joint preregistration before any upgrade branch: https://github.com/j4groupfounders/j4-upgrades-harness/commit/b7b853919779e2e5780774da7815b996dff12d45.
Frozen baseline SHA f6edeb4d13328b75e9e75eff34676bae751dad07; https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37727411400.

## Verdict
All preregistered protocol criteria pass.
Baseline: 51 tests, 0 skips. Accepted upgrades require unchanged named test inventory and no new skips.
Upgrade: https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37728401244.
Seeds: https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37728641573.
Project detections 4/5; combined 5/5; all seed infrastructure clean=True.
Batch 6 scoring retained: >=4/5 combined AND combined misses <=half project misses; infrastructure failures never count.
9 workflow runs (cap 12 including baselines), 6.57 actual job-minutes. Five separate fresh-checkout seed jobs. Explicit pipefail, public standard Linux Actions only.
Zero human app/test logic edits. No paid APIs/services, no model API calls by scripts, no customer/upstream contact. Session token cost unavailable, not claimed as zero measured cost.

## Migration, repairs, and limits
Baseline repairs: replaced upstream beta/dev DAMA and fixture-bundle constraints with stable 8.0.2/3.5.1 and locked PHPUnit 9.6.22 in Composer. Stable framework resolution is 6.4.47. PHP built-in HTTP server required variables_order=EGPCS to honor test environment; otherwise it rendered a dev toolbar. Clean replay exposed generated HTML Page/Fragment clock comments and only the RSS channel pubDate; those exact fields are normalized before preregistration, preserving item publication dates and content. Existing 51 tests/113 assertions pass. Deprecation warnings excluded from acceptance, no test assertions changed.
Migration so far: Symfony framework components 6.4→7.4.0, PHP>=8.2, removed framework annotations/handle_all_throwables options, migrated Route annotation namespace to Attribute\Route without changing route definitions. First major run retained exact frozen public HTTP but six authenticated form tests errored; application diagnostic logs added to artifact capture, not acceptance probes.
Captured logs proved Twig bridge latest 7.4 patch called setResourceInheritability absent from pinned Form 7.4.0. Aligned twig-bridge to 7.4.0, preserving the preregistered major target and all form/test logic.
Accepted clean-checkout frozen dependency replay 37728401244 preserved the exact committed lock bytes, complete named test inventory and all frozen HTTP snapshots. No classified HTTP changes needed. All application/test logic remains unchanged apart from Symfony route-import namespace migration; agent dependency/runtime/config repairs only.
FINAL GREEN: project detection 4/5, combined 5/5. Reversed post ordering escaped the project suite but changed frozen blog/RSS HTTP snapshots; the other four faults produced specific assertion/403 failures. All five infrastructure=false. Nine total workflow runs.

See PREREG.md and immutable fault list in harness. Full existing project suite, five frozen unauthenticated HTTP routes. No overall coverage or production certification claim. Teaching/reference apps, not random customer selection.
Tests/fixtures are retained; all agent migration/config edits itemized in upgrade.patch. Symfony deprecation warnings excluded, not assertions. No post-hoc probes or changed faults.

## Seed outcomes
- 0: weak CLI passwords accepted — project=True, HTTP=False, combined=True, infrastructure=False; 
- 1: search excludes matching titles — project=True, HTTP=True, combined=True, infrastructure=False; 
- 2: blog ordering reversed — project=False, HTTP=True, combined=True, infrastructure=False; 
- 3: comment persistence corrupts text — project=True, HTTP=False, combined=True, infrastructure=False; 
- 4: admin access denied to administrators — project=True, HTTP=False, combined=True, infrastructure=False; 

## All CI runs
- https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37726882265 — j4/p2g-baseline, failure, 0.53 job-min, SHA 76de25476a368fb39e3210714ddcb14321623655.
- https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37727060660 — j4/p2g-baseline, success, 0.35 job-min, SHA 5040eacdd73f9bf3321a1d3d196852d59f10b190.
- https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37727264424 — j4/p2g-baseline, failure, 0.55 job-min, SHA 204803fe4b9bd2eaeb68aee34442b927e1000842.
- https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37727411400 — j4/p2g-baseline, success, 0.35 job-min, SHA f6edeb4d13328b75e9e75eff34676bae751dad07.
- https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37727562145 — j4/p2g-upgrade, failure, 0.42 job-min, SHA 8253ee6d436e44b5b743416f368e34dfb204ad59.
- https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37727833958 — j4/p2g-upgrade, failure, 0.88 job-min, SHA 00311b391ed210531d3d5286951be5be1e2d7754.
- https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37728129736 — j4/p2g-upgrade, success, 0.50 job-min, SHA ae35d9ad0bdf87704ffcaf2307f4e1b7109b95e1.
- https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37728401244 — j4/p2g-upgrade, success, 0.40 job-min, SHA f4e3326b874017b76112b551d1f3c2f158f57e05.
- https://github.com/j4groupfounders/j4-p2g-symfony-demo/actions/runs/37728641573 — j4/p2g-seeds, success, 2.58 job-min, SHA eabf0834baf80ac9226e06df039b4fa20837e94b.

## Upgrade diff scope

.github/workflows/j4-p2g.yml            |    3 +
 composer.json                           |   53 +-
 composer.lock                           | 1989 +++++++++++++++++--------------
 config/packages/framework.yaml          |    2 -
 src/Controller/Admin/BlogController.php |    2 +-
 src/Controller/BlogController.php       |    2 +-
 src/Controller/SecurityController.php   |    2 +-
 src/Controller/UserController.php       |    2 +-
 8 files changed, 1124 insertions(+), 931 deletions(-)
