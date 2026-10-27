# From satellite snapshots to landscape systems

## The practical change

The next step is not another presentation. It is to connect terrain, water, fields and dispersed sites in a traceable GIS, while keeping observations separate from historical interpretations. The Angkor package is a portable starting point for this work, not the completed archaeological landscape database.

## What the papers contribute

| Reading | What to take from it | Consequence for this project |
|---|---|---|
| Van Liere, *Traditional Water Management in the Lower Mekong Basin* (1980), pp. 265-280; especially Figs. 2 and 4-7 | Landform and different ways of retaining, spreading or using water matter. Floodplain cultivation and bunded low-terrace fields are not interchangeable. | Compare landform settings, rather than calling every green field irrigated or every water feature a reservoir. His strict separation of monumental/religious and agricultural hydraulic works is an argument to examine, not an accepted classification rule. |
| Van Liere, *Mon-Khmer Approaches to the Environment* (1989), particularly pp. 152-154, Figs. 9.6-9.7 | The Sukhothai discussion distinguishes the low terrace/fossil alluvial fan and hill-fed landscape from the Yom River lowlands. | Examine west-east terrain and drainage relationships at Sukhothai. The chapter's ethnic, political and functional interpretations require other evidence; field geometry alone cannot establish them. |
| Evans et al., *A comprehensive archaeological map ... at Angkor* (2007), pp. 14277-14282; Fig. 2 and Mapping section | The mapped settlement extends beyond the major monuments. The authors used watershed boundaries for their 2,848 km2 survey and combined multiple sources. They also distinguish uncertain linear features from definitively identified canals or roads. | Retain our 1,999.8784 km2 comparison box, but establish a separate landscape-context extent using catchments and mapped settlement evidence. Add provenance and verification status to individual features. Do not copy their archaeological confidence onto our coarser imagery. |
| Groslier, *La cité hydraulique angkorienne: exploitation ou surexploitation du sol?* (1979), maps 1-7, pp. 196-202 | Rivers, spot heights, reservoirs, dispersed temples and proposed water redistribution are interpreted together. Maps 2-6 also distinguish historical stages. | Study source-to-storage-to-downstream relationships, not just distance to water. These are historical reconstructions, not measured 2025 irrigated extents. Do not trace the shaded areas into our GIS as validated polygons. |
| Hawken and Cobo Castillo, *Angkor's Agrarian Economy: A Socio-Ecological Mosaic*, opening pp. 338-340 | Productive open spaces are part of the settlement, not empty background. The authors emphasise a patchwork of management strategies rather than one uniform system. | Keep fields and their landform settings central. Avoid assuming that all similar field patterns had the same function, date or management regime. |
| Evans, *The Predicament of Archaeological Lidar: Perspectives from Southeast Asia*, supplied manuscript, pp. 17-18, 26, 36-37 | Existing knowledge, suitable data and explicit interpretation records matter. Page 26 specifically discusses interpreter identity and digitising scale. | Record source, interpreter, scale, confidence and supporting evidence. Our coarse surface model cannot be treated as archaeological lidar. The filename says “2019”, but publication year is not verified from the supplied manuscript. |

### The disagreement is useful

Van Liere's 1980 argument challenges Groslier's interpretation of the major hydraulic works. Evans et al. (2007) report later mapping and survey evidence for an integrated system, without resolving every feature's function or chronology. The Hawken chapter adds a more varied agrarian picture. We should not force the authors into agreement, or claim that two seasonal satellite composites settle this debate.

Groslier's map 7 labels a reconstructed archaeological lake margin at approximately +16 m. This is not a licence to threshold our modern DSM at 16 m: source datum, historical lake conditions, positional accuracy and interpretation would first need checking.

The Isanapura example in Van Liere is Sambor Prei Kuk, not Srei Santhor. It is an analogy, not evidence that the same mapped features occur at our Srei Santhor site.

## A concrete order of work

1. **Inspect the Angkor comparison core in QGIS.** Confirm that water, WorldCover 2021, 2025 imagery, FTW predictions and surface heights are clearly distinguished. This is also a GIS practice dataset.
2. **Establish a wider Angkor context.** Use the Puok, Siem Reap and Roluos drainage systems shown in the papers to guide acquisition of native DEM coverage. Delineate and check catchments, rather than drawing another temple-centred box. Keep any provisional boundary visibly provisional.
3. **Check terrain before combining DEMs.** Audit datum, masks, surface bias and native grids. Compare a second suitable source over hills, forest, built-up areas and open lowlands. Retain source differences; do not average them by default. See Terrain_audit.md.
4. **Build a sourced feature register.** For temples, reservoirs and linear features, retain original name, feature type, source URL/page/figure, coordinates and positional uncertainty, period evidence, interpreter, digitising scale and verification status. Modern places of worship and ancient remains must not be merged merely because their names contain wat or candi. Map-search results are leads, not archaeological dating evidence.
5. **Compare relationships at a defensible scale.** Start with broad elevation profiles, seasonal-water position and landscape setting. Distinguish proximity, plausible terrain connection and documented hydraulic connection. Reserve ancient/modern attribution for sourced evidence.
6. **Apply the structure to the other regions.** Sukhothai needs hills/fan/Yom-plain context; Srei Santhor needs the correct Tuol Basan location and floodplain units; Prambanan needs volcanic-slope/drainage context and a sourced candi inventory. Do not simply transfer an Angkor classification.

The folder currently contains an interim Angkor pilot. The other three GIS packages and the wider landscape work remain pending.


## Coverage of these working summaries

These are working literature summaries for discussion, not a personal reading-completion log or a claim of completed archaeological research.

- Van Liere 1980: text and relevant landform/Angkor map examples reviewed.
- Van Liere 1989: text review, with the Sukhothai page and relevant mapped examples inspected visually; some extracted text is noisy.
- Evans et al. 2007: article text and regional map reviewed.
- Groslier 1979: all seven map plates and captions reviewed visually. The full scanned French text has not yet been fully reviewed.
- Hawken and Cobo Castillo chapter: opening pages 338-340 reviewed, not the whole chapter.
- Evans lidar manuscript: selected sections, particularly PDF pages 17-18, 26 and 36-37, reviewed; not the whole manuscript. Publication year is unverified from the supplied copy.

No catchment delineation, DEM fusion, validated drainage model, sourced temple inventory, feature dating or accepted 2025 agricultural-area estimate is claimed. The separate terrain audit characterises existing cached surface models, not independently measured terrain accuracy.

## References supplied for the project

- Van Liere, W. J. (1980). Traditional Water Management in the Lower Mekong Basin. World Archaeology 11(3), 265-280.
- Van Liere, W. J. (1989). Mon-Khmer Approaches to the Environment. Chapter 9 in Culture and Environment in Thailand, Siam Society symposium volume. Cited examples on printed pages 152-154.
- Evans, D., et al. (2007). A comprehensive archaeological map of the world's largest preindustrial settlement complex at Angkor, Cambodia. PNAS 104(36), 14277-14282. https://doi.org/10.1073/pnas.0702525104
- Groslier, B.-P. (1979). La cite hydraulique angkorienne: exploitation ou surexploitation du sol? Bulletin de l'Ecole francaise d'Extreme-Orient 66, 161-202. Maps 1-7 on printed pages 196-202.
- Hawken, S., and Cobo Castillo, C. Angkor's Agrarian Economy: A Socio-Ecological Mosaic. Supplied book chapter, opening pages 338-340. https://doi.org/10.4324/9781351128940-24
- Evans, D. The Predicament of Archaeological Lidar: Perspectives from Southeast Asia. Supplied manuscript; publication details to be confirmed.

The original papers are already held by the recipient and are not duplicated here. Page references are printed article/chapter pages unless described as PDF pages. Source-specific interpretations above are not newly verified landscape attributes.
