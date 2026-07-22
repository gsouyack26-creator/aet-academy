# AET Academy - Build Changelog

Automation Engineering Technology training kiosk - single-file offline HTML trainer.
Steady build: 19 modules, 107 glossary terms, 5 tracks, 22 achievements, 137 flashcards, 11 simulators, 171-question exam pool.

> Note: this changelog was reconstructed on 2026-07-21 after the original file was
> lost to a text-encoding write error (no VCS backup). Entries v11.13-v12.12 are
> reconstructed in detail from build notes; releases v1.0-v11.12 established the core
> platform (the 19-module curriculum, glossary, flashcards with spaced repetition,
> final/module/skills exams, simulators, certificate, multi-user kiosk with team
> roster, achievements, XP/ranks, reference library, training plan, and the full
> download/print/copy export suite).

## Changelog (newest first)

### v13.46 &mdash; 2026-07-22
- **Simulators now require real interaction for credit.** Opening the Simulators page used to auto-credit XP for every simulator, because the page ran each sim&#39;s calculation once to populate its initial output. A new `_simSilent` guard suppresses crediting during that startup pass (wrapped in try/finally so it always resets), so you only earn XP + a &#10004; on a sim once you actually change an input or interact with it.

### v13.45 &mdash; 2026-07-22
- **Completed-module checkmark.** The collapsed module list in Learn now shows a green &#10004; next to any module you&#39;ve finished, so completed modules are obvious at a glance without expanding a track.
- **Role picker hints.** The sign-in gate and profile role pickers now explain each role: hover any chip for a tooltip, and a caption under the picker describes the selected role. Clarifies that Trainee/Technician are display/grouping labels while **Lead** unlocks the Team Roster, module assignment &amp; reports.

### v13.44 &mdash; 2026-07-22 &mdash; Level-aware Question of the Day + Sign-out relocated
- **Question of the Day now scales to the learner's level.** A day-one trainee only gets Foundations questions &mdash; harder tracks unlock as they rank up (Foundations &rarr; Field Devices &rarr; Systems &amp; Control &rarr; Reliability &amp; Career &rarr; Safety &amp; Advanced, ~one track per two levels). Any module you have completed or been quizzed on is always in the pool, so you are never asked advanced material you have not studied. The card now shows a &#127919; rank badge (e.g. "Apprentice level").
- The answered-state is now pinned to the exact question (stores module + question index), so feedback stays stable even if your pool changes during the day.
- **Sign-out button moved to its own full-width row** at the bottom of the sidebar. It was cramped in the icon toolbar and wrapping to two lines; the five tool icons (theme / text size / contrast / search / shortcuts) now sit in a centered wrapping row (`#sbtools`) with a clean full-width Sign-out button beneath them (red on hover).
- Verified: 15/15 QOTD level-gating VM checks (L1&rarr;foundations only, L3&rarr;+field, L10&rarr;all incl. advanced, completed/scored modules join pool, badge renders, feedback stable) + 8/8 sign-out layout checks.

### v13.43 &mdash; 2026-07-22 &mdash; Ladder &amp; ST Lab goes LIVE-GRADED
- Ported Code Armory's Structured-Text runtime (`runSt`) into the Ladder &amp; ST Practice Lab. The 138 challenges now grade three ways:
  - **Structured Text (60):** type ST code, hit **Run &amp; Check** &mdash; your program executes against real test cases (set inputs, run scans, assert outputs) and you get a pass/fail table plus XP when all cases pass.
  - **Troubleshooting (28):** type your diagnosis; it is normalized-matched against the accepted fault/fix answers.
  - **Ladder (50):** worked-solution reveal (guided).
- New filter bar (All / Ladder / Structured Text / Troubleshooting) with live counts; grading dispatch is flag-based (`stGrade` / `mode:predict`) so every live-gradable challenge shows its runner.
- Runner supports the ST subset: `:=`, IF/ELSIF/ELSE, CASE, FOR/WHILE/REPEAT, arrays, arithmetic, comparison, boolean ops, MIN/MAX/ABS. (Timer/function-block challenges stay guided.)
- Verified: 21/21 headless VM checks (138 labs = 60 ST + 28 predict + 50 guided; runSt live-grades `st-intro` correct=PASS 2/2, wrong=FAIL; predict + filters).

- **v13.42** &mdash; NEW: *Ladder &amp; Structured Text Practice Lab* &mdash; 96 hands-on exercises ported from the CodeForge "Ladder Logic" track (80 ladder + 16 Structured Text). Allen-Bradley / Studio 5000 style ladder (XIC/XIO/OTE, latches, timers, counters, sequencers, PID) and IEC 61131-3 Structured Text. New top-level nav item (#ladderlab) with All / Ladder / Structured Text filters; each exercise shows prompt + lesson, a scratch code box, and a reveal-solution + explanation. New data file ladder_labs_data.py (LADDER_LABS) + renderLadderLab view.

- **v13.41** &mdash; NEW MODULE 22: *Amazon Robotics &amp; Autonomous Mobile Robots (AMR)* (module id 21, added to the Systems &amp; Control track). Covers how an AR floor works (fiducials, pods, highways, charging), drive-unit models (Hercules/Atlas/Titan/Pegasus + legacy series) and service tools (ARTS, DUDT wheel-wear < 190/195 mm), charge management (drive:charger 26:1 Sev-3 threshold, LCRM/MDIPF), and top floor faults (error 105 fiducial, 206 wheel obstruction, No Comms/VLAN, charger Output Overcurrent). Includes AR floor PM tiers, a safe-entry safety note, an 8-question quiz, and a "Triage an AR Drive Disablement" lab. Total modules 21 &rarr; 22.

- **v13.40** &mdash; NEW MODULE 21: *Material Handling &amp; Conveyor Systems (MHE)* (module id 20, added to the Field Devices &amp; Drives track). Covers conveyor types (belt, MDR, accumulation, merge/divert, gapper), 24 VDC Motor-Driven Roller zones and Zero-Pressure Accumulation (ZPA), sortation technologies (sliding-shoe, cross-belt, tilt-tray), and the most common MHE faults (back-pressure timeout, jams, divert-gate solenoid, ADTA E-stop-open recovery, belt mistracking). Includes ACY1 belt-tracking / screw take-up rules, an 8-question quiz, and a "Map a ZPA Zone" lab. Total modules 20 &rarr; 21.

- **v13.39** &mdash; NEW MODULE 20: *PLC Programming Languages &mdash; Ladder vs Structured Text (IEC 61131-3)* (module id 19, added to the Foundations track after PLC Programming II). Covers the five IEC 61131-3 languages, core Ladder instructions (XIC/XIO/OTE/OTL/OTU, timers, counters), core Structured Text (:= vs =, &lt;&gt;, IF/CASE/FOR/WHILE, SCL), a language-selection decision table, and an ACY1/AWCS grounding section (ladder+AOIs per zone, 3-task model, F0xx watchdog fault from runaway FOR-DO loops). Includes an 8-question quiz and a "Translate a Rung Both Ways" lab. Total modules 19 &rarr; 20.

- **v13.38** - Resource Library: quick jump-to-module chip row scrolls straight to any module's resources in the grouped list.
- **v13.37** - Training Plan: &#128202; Download .csv export (order, module, title, minutes, day, complete-by) for supervisors/spreadsheets.
- **v13.36** - Command palette: quick actions to study your weakest module (flashcards) and challenge your weakest track (arcade).
- **v13.35** - Training Plan: &#127937; Projected track finish dates section shows a completion date per track at your current pace.
- **v13.34** - Lab Simulators: &#127919; Reinforce your weakest track card recommends a hands-on sim from your lowest-scoring track.
- **v13.33** - Module page: &#128203; Recommended first card flags earlier unfinished modules in the same track before you dive in.
- **v13.32** - Quiz Arcade: &#127919; Recommended challenge banner starts a timed run on your weakest track (lowest quiz average).
- **v13.31** - Flashcards: &#128201; Weakest module cards button jumps straight into module flashcards for your lowest-scoring module.
- **v13.30** - Training Plan: &#127919; Today&#39;s session card lists the modules that fit today&#39;s pace budget with a Start button.
- **v13.29** - Module page: &#128300; Related lab simulators card links matching-track sims (jump to #sims + scroll to the sim).
- **v13.28** - Search now offers &#128161; "Did you mean?" suggestions when a query returns no matches - trigram-overlap fuzzy matching against glossary terms and module titles (tolerates typos), each a one-tap link that reruns the search.
- **v13.27** - Achievements "Next to aim for" now targets the badge you're *closest* to earning (by progress ratio) and shows a live progress bar with an N/M count for quantifiable badges (modules, streak, aced quizzes, flashcards, sims, bookmarks, module exams).
- **v13.26** - Glossary adds a &#127919; "Quiz my weak spot" button that auto-picks your weakest quizzed module (with enough terms) and launches a module-filtered Term-Match quiz - one tap to drill the vocabulary you're shakiest on.
- **v13.25** - Module score card now nudges you toward a perfect run when you haven't aced the quiz yet ("ace all N for the &#11088; star"), turning the aced-star achievement into a visible goal on every module you've quizzed but not perfected.
- **v13.24** - Final-exam readiness card now pinpoints your &#128161; "Biggest lift" - the lowest of coverage / quiz-confidence / flashcard-mastery - with a one-tap action to close that specific gap (only while you're below the 80% pass line).
- **v13.23** - Dashboard daily-goal card now surfaces due flashcards when your goal isn't met yet (&#128196; "N flashcards due now" with a one-tap jump to review), turning spaced-repetition due-cards into an actionable way to hit today's goal.
- **v13.22** - Simulator activity panel now nudges you toward tools you haven't opened yet with a &#129514; "Not tried yet" line (top untried sims, click to jump), so you keep exploring the full lab.
- **v13.21** - Resource Library now leads with a &#128204; "Resources for your next module" spotlight (the next incomplete module's top links) so learners see relevant free resources before diving in.
- **v13.20** - Certificate page shows an actionable &#9201;&#65039; "Left to unlock" estimate (remaining modules with ~minutes + the final exam) until all requirements are met.
- **v13.19** - The flashcard Leitner box-distribution card now leads with a mastery milestone: &#127891; how many cards you've mastered and the percentage of the deck, with a full-deck-mastered celebration at 100%.
- **v13.18** - The Learn page now spotlights the track you're closest to finishing (3 or fewer modules left), with a direct link to the next module in it.
- **v13.17** - The Notes page now nudges you about modules you've completed but not yet noted, with quick links to add a field tip before the details fade.
- **v13.16** - Glossary module-filter dropdown now shows the term count per module (e.g. "Module 3: Sensors (9 terms)"), so you can see at a glance which modules have quizzable vocabulary sets.
- **v13.15** - Weak Spots cards now offer a &#129504; Quiz terms button on any weak module that has 4+ glossary terms, launching a module-filtered Term-Match quiz for fast vocabulary remediation.
- **v13.14** - The module page's &#128221; Module exam best card now shows the date your best score was set, surfacing the stored timestamp.
- **v13.13** - Lab Simulators activity panel now highlights your &#128295; most-practiced tool (the sim you've opened most) when you've used 2+ tools with 2+ runs.
- **v13.12** - Profile track breakdown now leads with an insight line: &#127942; your strongest track (highest quiz accuracy) and &#128201; the track to focus on (lowest), shown when you have quiz scores in 2+ tracks.
- **v13.11** - Term-Match quiz launched from a module now loops back to that module: results screen adds a &#128218; Review Module button and Play-again re-runs the same module filter.
- **v13.10** - Module page: Quiz-these-terms button launches a Term-Match quiz filtered to the module's glossary terms.
- **v13.09** - Module page: key-term chips now show the term definition on hover (title tooltip).
- **v13.08** - Weak Spots: Start-here callout highlights your single weakest module with a direct review link.
- **v13.07** - Profile: Module exams passed stat card (count of module exams scored 80%+ out of all modules).
- **v13.06** - Certificate: credential now notes how many modules were mastered with a perfect quiz score.
- **v13.05** - Sims: checklist adds a Try-next quick-jump to the first untried tool (and an all-explored celebration).
- **v13.04** - Learn: course-progress card now shows how many tracks are fully complete (&#127941; N of M).
- **v13.03** - Profile: overall Quiz accuracy stat card (earned/possible across all scored modules, with quizzed count).
- **v13.02** - Module page: More in this track card lists sibling modules with completion status and quick links.
- **v13.01** - Flashcards: &#128293; Cards to focus on section lists studied cards still stuck in box 1-2, sorted by box.
- **v13.00** - Dashboard now spotlights your weakest track (lowest quiz average) with a one-tap Review link, so you always know where a little study pays off most.
- **v12.99** - Training Plan header now shows a Modules left stat (remaining count, of total, and how many are done).
- **v12.98** - Module pages now warn you when you have questions flagged for review from a past attempt, prompting a quiz retry.
- **v12.97** - Final exam results now include a Focus your review card listing the modules where you missed questions, sorted by most-missed, with jump-to-module links.
- **v12.96** - Achievements page now shows how many badges you earned in the last 7 days.
- **v12.95** - The study-activity heatmap now calls out your busiest study day and its minutes.
- **v12.94** - Resource Library header now shows how many of the 19 modules have free resources.
- **v12.93** - The completion certificate now notes how many days of study your credential represents (from your first session).
- **v12.92** - Profile now shows a Learning since stat with the date of your first study session.
- **v12.91** - On the Learn page, hovering a completed module's status dot now shows the date you finished it.
- **v12.90** - The printable Module Record transcript now has a Completed column showing the date each module was finished.
- **v12.89** - Completed modules now show the date you finished them on the module page.
- **v12.88** - Dashboard weekly digest now shows how many modules you completed this week, tracked by a new completion-date record.
- **v12.87** - Term Match glossary quiz now tracks how many times you've played and shows the count on your results.
- **v12.86** - Practical Skills Exam now shows a New personal best! banner (or your previous best) on results, completing best-score tracking across all four exams/quizzes.
- **v12.85** - Module exam results now show a New personal best! banner (or your previous best) so retakes track your improvement, matching the final and Term Match quizzes.
- **v12.84** - Simulator activity panel now shows your total run count across all tools alongside the per-tool attempt breakdown.
- **v12.83** - Learn page now shows a gold star next to modules you aced (perfect quiz score) so your mastered modules stand out at a glance.
- **v12.82** - Glossary Term Match button now shows your best score (e.g. best 90%) right on the button so you can see your record before playing.
- **v12.81** - Final Exam intro now shows your exam-readiness gauge (module coverage + quiz confidence + flashcard mastery) until you pass, so you can gauge whether to study more first.
- **v12.80** - Added an L keyboard shortcut to jump straight to the Learn (modules) page, listed in the keyboard shortcuts help.
- **v12.79** - Achievements page now spotlights a Next to aim for badge (the next locked achievement plus how to earn it) to give you a concrete goal.
- **v12.78** - Profile stats grid now includes a Perfect quizzes card counting the module quizzes you aced (100%).
- **v12.77** - Weekly digest now projects a finish estimate: at your current pace (min/active day), it shows the lessons left and roughly how many more study days to complete the course.
- **v12.76** - Module breadcrumb now shows your track completion (e.g. Controls - 3 of 5 - 60% done) so you can see progress within each track at a glance.
- **v12.75** - Certificate page now shows a Certificate readiness progress bar (modules + final exam) on the requirements card, with an All-requirements-met note at 100%.
- **v12.74** - Module pages now show a Module N of 19 position indicator in the header meta line so you always know where you are in the course.
- **v12.73** - Dashboard weekly digest now shows a Last studied: today / yesterday / N days ago line, with a gentle welcome-back nudge after a 2+ day gap.
- **v12.72** - Glossary Term Match quiz now records your best score and shows a New personal best / Your best: N% line on the results screen.
- **v12.71** - Command palette: Profile - copy my stats and Profile - print transcript entries added.
- **v12.70** - Achievements: a nudge under the collection bar shows how many badges remain for a full set.
- **v12.69** - Sims page: the intro tool count is now derived from the live simulator list so it never drifts.
- **v12.68** - Learn page: filter chips now show live counts (All / Not started / In progress / Done / Noted).
- **v12.67** - Command palette: Weak Spots - start focused drill entry (shown when you have weak spots) jumps in and launches the drill.
- **v12.66** - Weak Spots: shows an estimated review time to work through all your weak modules.
- **v12.65** - Module page: shows your module-exam best score (color-coded passed / keep-going) when you have attempted it.
- **v12.64** - Learn page: Continue button jumps straight to your next unfinished module (hidden once the course is complete).
- **v12.63** - Profile: added Total study time and Days studied stats to the stats grid (lifetime totals).
- **v12.62** - Dashboard: This-week digest now shows a lifetime study summary (total time studied across N days).
- **v12.61** - Profile: the Day-streak stat now shows your personal best (Day streak - best N) so your record is visible at a glance.
- **v12.60** - Dashboard: personal best day-streak tracker - remembers your longest streak and shows it in the streak-milestones card when your current streak is below it.
- **v12.59** - Command palette: Roster: copy team summary entry (Lead-gated) jumps to roster and copies the ranked team summary.
- **v12.58** - Roster (Lead): Copy roster summary button - copies a ranked team text summary (learners, avg completion, exam-certified, active-today, per-learner done/level/badges/streak/exam) to clipboard.
- **v12.57** - Learn page: companion "Download syllabus" button saves the course outline as a plain-text file (aet-course-syllabus-DATE.txt) - matches the syllabus printout for offline archiving.
- **v12.56** - Command palette: new "Learn: print course syllabus" entry runs the new syllabus printer from anywhere.
- **v12.55** - Learn page: new "Print course syllabus" button opens a printable one-page course outline (learner + date, per-track sections, every module's title / estimated time / quiz count / objectives) - instructor-ready.
- **v12.54** - Achievements page now shows a "Latest badge" callout at the top (icon, name, earned date) highlighting your most recently unlocked achievement.
- **v12.53** - Dashboard "This week" digest now shows a line summarizing how many of the last 7 days hit your daily study goal (e.g. "Daily goal met on 3 of 7 days"), highlighted green when at least one day was met.
- **v12.52** - Learn page: each track header now shows a done/total module count (e.g. "2/4 modules") next to the percentage, so progress within a track is visible at a glance.
- **v12.51** - Global keyboard shortcuts: press G to jump to the Glossary and H to jump to the Dashboard (home); added both to the ? shortcuts help. Guarded so typing in inputs/on the login gate is unaffected.
- **v12.50** - Notes page: search now shows a "Showing N of M notes for &lt;query&gt;" count line above matching notes (hidden with no query / zero matches).
- **v12.49** - Weak Spots page gains a &#128203; Copy weak topics button + copyWeakSpots() that copies your weak-module list (id, title, score/percent, flagged count) as a ready-to-use study to-do list.
- **v12.48** - Glossary Term of the Day now has a &#128266; Hear it button (text-to-speech, shown only when the browser supports it) for parity with the dashboard term-of-day.
- **v12.47** - Practical Skills Exam result now has a &#128203; Copy result button + copySkillsResult() (technician name, score/percent, pass/Field-Diagnostician status, date) for parity with the final-exam result view.
- **v12.46** - Quiz Arcade bests summary now shows your Average best accuracy across all challenges you've set a personal best in, alongside the existing strongest-track callout.
- **v12.45** - Resource Library now shows a Showing N of M resources for &ldquo;query&rdquo; count line when a search is active (hidden with no query or zero matches), matching the Learn/Glossary search-count pattern.
- **v12.44** - Module page key-terms card gains a &#128203; Copy terms button + copyModuleTerms() that copies the module's key glossary terms *with their definitions* (module-titled header + count) to the clipboard.
- **v12.43** - Leaderboard now shows a You're Nth of M position banner (per selected metric) with the gap to the person one rank ahead, or a leading-the-board message when first; hidden when you're the only learner.
- **v12.42** - Command palette gains a &#128203; Reference: copy booklet entry that jumps to the Reference Library and copies the full booklet, matching the existing download/print palette commands.
- **v12.41** - Reference Library gains a &#128203; Copy booklet button + copyRefBook() that copies all reference cards (pinned-first, category-ordered, with a card-count header) to the clipboard, mirroring the Download .txt booklet format.
- **v12.40** - Quiz Arcade results now show a &#128218; Brush up on the modules you missed panel with review buttons for each module a wrong answer came from (deduped, sorted); hidden on a perfect score.
- **v12.39** - Command palette gains a &#128203; Certificate: copy credential entry (only when the certificate is earned) that jumps to the cert page and copies the shareable credential summary.
- **v12.38** - Certificate page: &#128203; Copy credential button + copyCert() copies a shareable text summary (name, course, exam/skills %, rank, credential ID, issue date) to clipboard; shown only when passed+all-modules-done.
- **v12.37** - My Notes page: &#128203; Copy all button copies every module note (learner header + per-module titles) to the clipboard, mirroring the Download .txt export.
- **v12.36** - Dashboard Term of the day now links to the module that covers the term (&#128218; Module N: Title), so you can jump from a daily vocab word straight into the lecture that teaches it.
- **v12.35** - Weak Spots page: each weak module now has a &#128218; Flashcards button (alongside Review module) that jumps straight into spaced-repetition flashcards for that module.
- **v12.34** - Learn page shows a "Showing N of M modules" count whenever a filter or search is active (names the query and offers a one-click clear), mirroring the glossary/reference/search result counts.
- **v12.33** - Final Exam history now shows a summary line above the attempt bars: Average / Best / Latest score plus a &#9650;/&#9660; trend indicator (percentage-point change since your first attempt).
- **v12.32** - Dashboard Question of the day now shows a &#128218; Review Module link under the answer feedback, jumping straight to the module the question came from so you can study the topic you just missed (or aced).
- **v12.31** - Dashboard Term of the day now has a &#9734; Save to favorites toggle (shows &#11088; Saved once starred) and a &#128266; Hear it button (when text-to-speech is available) to bookmark or speak the daily term without leaving the dashboard.
- **v12.30** - Training Plan: &#128197; Or finish by date picker - choose a target completion date and the plan auto-computes the required daily study pace (clamped 10-240 min) to hit it.
- **v12.29** - Training Plan: &#128203; Copy plan button copies the whole plan (learner, pace, total time, finish date + numbered module list with complete-by dates) to the clipboard for pasting into notes or email.
- **v12.28** - Training Plan: &#128197; Add to calendar (.ics) button downloads an iCalendar file with one all-day event per remaining module on its projected complete-by date (importable into Google/Outlook/Apple Calendar).
- **v12.27** - Recent searches: the Search page now remembers your last few successful queries (prefix-collapsed, capped at 6) and shows them as clickable &#128269; chips when the box is empty, with a Clear button.
- **v12.26** - Search category filter chips: when a query matches more than one category you get All / Lectures / Glossary / Reference / Notes chips (with counts) to narrow the results; the filter resets to All whenever the query changes and falls back to All if the chosen category becomes empty.
- **v12.25** - Search results now show a per-category breakdown next to the total (e.g. "26 results &middot; 14 lectures &middot; 5 terms &middot; 7 cheat sheets") whenever a query matches more than one category.
- **v12.24** - &#11088; Download starred cards: a downloadStarredCards() export writes only your starred flashcards to aet-starred-flashcards.txt; a Download-starred button appears in the Flashcards toolbar whenever you have starred cards.
- **v12.23** - Dashboard TODAY&#39;S REVIEW card now shows a &#11088; Review-starred button (in both the cards-due and all-caught-up states) when you have starred flashcards; new studyStarred() helper jumps straight into the starred deck.
- **v12.22** - Command-palette discoverability: added a &#11088; "Flashcards: study starred cards (N)" command (shown only when you have starred cards) and a &#127922; "Learn: surprise me" command that opens a random module.
- **v12.21** - Flashcard <b>S</b> keyboard shortcut stars/unstars the current card (guarded off in module-study mode); added to the keyboard help modal and the on-card hint line.
- **v12.20** - &#11088; Study-starred flashcard mode: a Study starred (N) button (shown when you have starred cards) drills only your starred deck via a new buildFcOrder('star') filter; includes a mode label, Back-to-due button, and a friendly empty-state.
- **v12.19** - Flashcard star/favorites: &#9734; Star / &#11088; Starred toggle on each flashcard (persists in S.fcStars by card key), a live starred count in the Flashcards header, and defensive init for older saved states.
- **v12.18** - Module Exam flag-for-review: each question gets a &#128681; Flag toggle while taking the exam, and the sticky progress bar shows a Jump-to-flagged (N) scroll button (mirrors the Final Exam flag feature from v12.12).
- **v12.17** - Learn page &#127922; Surprise me button: opens a random module you have not finished (falls back to full pool when all done), with a toast of the picked module title.
- **v12.16** - Reference Library search now shows a "Showing N of M cheat sheets" match count when a search term or category filter is active.
- **v12.15** - Glossary "Showing N of M terms" count now also appears for the A-Z letter filter and names the active module (e.g. "Module 5: Robotics") when filtering by module.
- **v12.14** - Flashcard module-study view gains a "Back to module" button, closing the navigation loop with v12.13's "Study as flashcards".
- **v12.13** - Module page "Study as flashcards" button (modules with quiz cards) jumps straight into flashcard module-study mode for that module (studyModuleFlash).
- **v12.12** - Final Exam flag-for-review: per-question Flag toggle + sticky-bar "Jump to flagged (N)" scroll button (toggleExFlag/jumpFlagged, EX.flags).
- **v12.11** - Glossary favorite count on the Favorites-only and Quiz-favorites buttons, e.g. "Favorites only (12)" (hidden when zero).
- **v12.10** - Dashboard Track-progress card shows a Next: hint under each incomplete track (next unfinished module title, click to jump).
- **v12.09** - Glossary Clear-filters button appears whenever any filter is active (search / A-Z / favorites / module) and resets all four (clearGlossFilters).
- **v12.08** - "Quiz this module" button on glossary when a module filter is active (glossQuizStart scoped to that module, needs >=4 terms).
- **v12.07** - Resource count shown in Resource Library card headers (respects the resource search filter).
- **v12.06** - Total course time on the Learn header; module/track counts now dynamic (MODS.length / TRACKS.length) instead of hard-coded.
- **v12.05** - Track-complete green checkmark on the dashboard Track-progress card when a track hits 100%.
- **v12.04** - Glossary filter-by-module dropdown (window._glossMod + glossMod()), filters the term list to one module.
- **v12.03** - Module counts (N/M and %) on the dashboard Track-progress card.
- **v12.02** - Resource count added to the module-page meta line.
- **v12.01** - Resource-count link badge on Learn module rows.
- **v12.00** - Milestone: Dashboard Track-progress overview card (mini bar + % per track, colored to the track, click to Learn).
- **v11.99** - "Noted" filter chip on the Learn filter bar (shows only modules you've taken notes on).
- **v11.98** - Key-terms count ("X of Y") on module pages.
- **v11.97** - Notes indicator badge on Learn module rows when a module has notes.
- **v11.96** - Per-track study-time-remaining on Learn track headers (switches to a Complete badge at 100%).
- **v11.95** - Jump-to-next-unanswered button on all three exams (final / module / skills).
- **v11.94** - Live answered-count progress on the Skills Exam.
- **v11.93** - Live answered-count progress on the Module Exam.
- **v11.92** - Live answered-count progress on the Final Exam (sticky progress bar).
- **v11.91** - Flashcard session progress bar (card X of Y).
- **v11.90** - Final-exam length picker (Quick 20 / Standard 40 / Full 171).
- **v11.89** - Track-complete badge on Learn track headers.
- **v11.88** - Study-time-remaining on the Learn course-progress card.
- **v11.87** - Command-palette entry: download complete study pack.
- **v11.86** - Download complete study pack (glossary + flashcards + reference + resources in one .txt).
- **v11.85** - Command-palette resource entries (download / copy / print resource list).
- **v11.84** - Print module-exam review sheet.
- **v11.83** - Module-exam review sheet (download + copy).
- **v11.82** - Copy final-exam review sheet.
- **v11.81** - Print final-exam review sheet.
- **v11.80** - Copy resource library list.
- **v11.79** - Print resource library.
- **v11.78** - Download final-exam review sheet (missed questions only).
- **v11.77** - Command-palette print actions (glossary / flashcards / reference).
- **v11.76** - Print flashcards study sheet.
- **v11.75** - Command-palette download entries (gloss favorites / flashcards / reference booklet).
- **v11.74** - Download reference booklet as .txt.
- **v11.73** - Download favorite glossary terms.
- **v11.72** - Download flashcards study sheet.
- **v11.71** - Copy module-exam result.
- **v11.70** - Download final-exam result.
- **v11.69** - Quiz favorites (glossary Term-Match deck from starred terms).
- **v11.68** - Module-exam timing (elapsed time in result banner).
- **v11.67** - Exam duration shown in the printed transcript.
- **v11.66** - Exam duration in the copied final-exam result.
- **v11.65** - Flashcard session grade tally (reviewed / good / hard / again).
- **v11.64** - Copy reference cards to clipboard.
- **v11.63** - Final-exam timing (total time and per-question average).
- **v11.62** - Hear reference cards (text-to-speech).
- **v11.61** - Copy study stats to clipboard.
- **v11.60** - Hear flashcards (text-to-speech).
- **v11.59** - Hear glossary terms (text-to-speech).
- **v11.58** - Command-palette glossary shortcuts (copy favorites / download .txt).
- **v11.57** - Copy favorite glossary terms.
- **v11.56** - Copy module notes.
- **v11.55** - Live word/char count on module notes.
- **v11.54** - Achievement earned dates.
- **v11.53** - Study Tip of the Day on the dashboard.
- **v11.52** - Term of the Day on the Glossary page.
- **v11.51** - Copy final-exam result.
- **v11.50** - Save all module key terms to favorites at once.
- **v11.49** - Command-palette entries (glossary random term, achievements copy).
- **v11.48** - Random glossary term.
- **v11.47** - Copy achievements progress.
- **v11.46** - Download resource list as .txt.
- **v11.45** - Resource Library search.
- **v11.44** - Course progress bar on the Learn header.
- **v11.43** - Flashcard session-length picker (10 / 20 / 30 / all).
- **v11.42** - Notes total word count in the My Notes header.
- **v11.41** - Glossary A-Z jump index.
- **v11.40** - Download glossary as .txt.
- **v11.15** - Simulator completion checklist (all 11 sims, tap to jump).
- **v11.14** - Glossary Term-Match quiz.
- **v11.13** - Notes search box in My Notes.
- **v11.1** - Team, assessment & retention pack (team leaderboard, per-module mastery, and more).
