<p align="center">
  <a href="https://www.loganmedwardsastrophy.com/"><img src="docs/banner.svg" width="100%" alt="Logan M Edwards, Astronomy and Astrophysics, Planetary Science"></a>
  <br/>
  <picture><img src="docs/typing.svg" width="482" alt="Asteroid catalogs and mining economics. Asteroid belt origins and Mars mapping. Deep learning on survey imagery. Orbit simulation in pure Python."></picture>
  <br/>
  <a href="https://www.loganmedwardsastrophy.com/"><img src="docs/links/website.svg" height="36" alt="Website: loganmedwardsastrophy.com"></a>
  <a href="https://www.loganmedwardsastrophy.com/Logan_Edwards_CV.pdf"><img src="docs/links/cv.svg" height="36" alt="CV (PDF)"></a>
  <a href="https://www.linkedin.com/in/logan-edwards-shf/"><img src="docs/links/linkedin.svg" height="36" alt="LinkedIn: logan-edwards"></a>
  <a href="https://www.kaggle.com/loggger"><img src="docs/links/kaggle.svg" height="36" alt="Kaggle: loggger"></a>
</p>

I'm an Astronomy & Astrophysics student at Florida Tech, double majoring in Planetary Science. Most of the work here is about asteroids. I built a catalog of about 1.57 million of them and a pipeline that estimates whether mining one would make money, then used the catalog for a [paper](https://github.com/loggger101/asteroid-belt-gradient) on whether the belt's S/C composition gradient is left over from when the planets formed. I've also trained two image classifiers and written an orbit simulator.

Outside of school I'm CTO of [AspireCURES](https://www.aspirecures.com), a company that matches patients with rare brain diseases to research, and VP of Database Management at [Sisters Hope Foundation](https://www.sistershopefoundation.org), a rare-disease nonprofit. I run the websites and patient databases for both.

<p align="center">
  <a href="#-space-economics">Space economics</a> · <a href="#-planetary-science">Planetary science</a> · <a href="#-deep-learning">Deep learning</a> · <a href="#-simulation">Simulation</a> · <a href="#-rare-disease-work">Rare-disease work</a> · <a href="#-elsewhere">Elsewhere</a> · <a href="#-every-commit-so-far">Commits</a> · <a href="#-languages">Languages</a> · <a href="#-passing-earth-this-week">Flybys</a> · <a href="#-get-in-touch">Contact</a>
</p>

<p align="center">
  <a href="https://github.com/loggger101/AsteroidCatalog"><picture><source media="(max-width: 600px)" srcset="docs/stats/catalog-compact.svg"><img src="docs/stats/catalog.svg" width="23.5%" alt="1.57M asteroids cataloged (AsteroidCatalog)"></picture></a>
  <a href="https://github.com/loggger101/asteroid-belt-gradient"><picture><source media="(max-width: 600px)" srcset="docs/stats/belt-compact.svg"><img src="docs/stats/belt.svg" width="23.5%" alt="161,659 classified asteroids analyzed (asteroid-belt-gradient)"></picture></a>
  <a href="https://github.com/loggger101/General_Research"><picture><source media="(max-width: 600px)" srcset="docs/stats/sources-compact.svg"><img src="docs/stats/sources.svg" width="23.5%" alt="605 research sources (General_Research)"></picture></a>
  <a href="https://github.com/loggger101/Hermes_Skills"><picture><source media="(max-width: 600px)" srcset="docs/stats/skills-compact.svg"><img src="docs/stats/skills.svg" width="23.5%" alt="253 agent skills (Hermes_Skills)"></picture></a>
</p>

<p align="center">
  <a href="https://github.com/loggger101/Satellite-Space-Flight"><picture><source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="docs/gallery/satellite-compact.webp"><source media="(prefers-reduced-motion: reduce)" srcset="docs/gallery/satellite.webp"><source media="(max-width: 600px)" srcset="docs/gallery/satellite-motion-compact.webp"><img src="docs/gallery/satellite-motion.webp" width="48.5%" alt="Satellite-Space-Flight: the ISS orbit, live elements and ground-station passes"></picture></a>
  <a href="https://github.com/loggger101/asteroid-belt-gradient"><picture><source media="(max-width: 600px)" srcset="docs/gallery/belt-compact.webp"><img src="docs/gallery/belt.webp" width="48.5%" alt="asteroid-belt-gradient: S-types give way to C-types farther from the Sun (fraction by number across semimajor axis, D of at least 53 km, families collapsed)"></picture></a>
  <a href="https://github.com/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data"><picture><source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="docs/gallery/mars-compact.webp"><source media="(prefers-reduced-motion: reduce)" srcset="docs/gallery/mars.webp"><source media="(max-width: 600px)" srcset="docs/gallery/mars-motion-compact.webp"><img src="docs/gallery/mars-motion.webp" width="48.5%" alt="Mars Global Mosaic: Ius Chasma in visible light, night-time infrared and spectral clusters, then SVM landform classes across Tharsis and Valles Marineris"></picture></a>
  <a href="https://github.com/loggger101/drone-target-id"><picture><source media="(prefers-reduced-motion: reduce) and (max-width: 600px)" srcset="docs/gallery/drone-compact.webp"><source media="(prefers-reduced-motion: reduce)" srcset="docs/gallery/drone.webp"><source media="(max-width: 600px)" srcset="docs/gallery/drone-motion-compact.webp"><img src="docs/gallery/drone-motion.webp" width="48.5%" alt="drone-target-id: per-target valid/invalid scores on aerial footage"></picture></a>
  <a href="https://github.com/loggger101/AsteroidCatalog"><picture><source media="(max-width: 600px)" srcset="docs/gallery/catalog-compact.webp"><img src="docs/gallery/catalog.webp" width="48.5%" alt="AsteroidCatalog: 952,026 main-belt proper orbits, the Kirkwood gaps and families"></picture></a>
  <a href="https://github.com/loggger101/star-spectral-classifier"><picture><source media="(max-width: 600px)" srcset="docs/gallery/star-compact.webp"><img src="docs/gallery/star.webp" width="48.5%" alt="star-spectral-classifier: spectral letters on held-out stars, true against predicted"></picture></a>
</p>

### <picture><img src="docs/icons/economics.svg" width="24" height="24" align="top" alt=""></picture> Space economics

The first four repos work together to estimate whether an uncrewed asteroid mining mission would turn a profit, and the fifth checks the pipeline against other people's code. The catalog also feeds my paper.

<p align="center">
  <picture><source media="(max-width: 600px)" srcset="docs/pipeline-compact.svg"><img src="docs/pipeline.svg" width="100%" alt="How the repos connect: General_Research holds the sources that AsteroidCatalog, spacecost and economicspace cite. AsteroidCatalog releases feed asteroid-belt-gradient, which builds the paper, and economicspace, which also installs spacecost, quietlaunch and quietqueue, cites the starred-repos audit, and ranks mining targets by profit."></picture>
</p>

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/economicspace">economicspace</a></b><br/><sub>the pipeline</sub><br/><sub>25,268 lines of code</sub><br/><sub>98,204 total lines</sub><br/><picture><img src="docs/sparks/economicspace.svg" width="120" alt="My commits to economicspace each week since August 2026"></picture></td>
    <td valign="top"><p>The main pipeline. It builds a catalog from public astronomy databases, prices the minerals, costs the transport, then runs the rocket equation and a cost cascade to rank targets by profit.</p><picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <picture><img src="https://img.shields.io/badge/pandas-1f3354?style=flat-square&logo=pandas&logoColor=white" alt="pandas"></picture> <picture><img src="https://img.shields.io/badge/Docker-1f3354?style=flat-square&logo=docker&logoColor=white" alt="Docker"></picture></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/AsteroidCatalog">AsteroidCatalog</a></b><br/><sub>Stage 1: the catalog</sub><br/><sub>5,701 lines of code</sub><br/><sub>13,599 total lines</sub><br/><picture><img src="docs/sparks/AsteroidCatalog.svg" width="120" alt="My commits to AsteroidCatalog each week since September 2026"></picture></td>
    <td valign="top"><p>The pipeline's catalog stage, moved into its own repo. About 1.57 million asteroids from JPL SBDB, SsODNet, NEOWISE and MP3C, cross-matched, with the source of every value recorded and a cited composition estimate for each taxonomy class. Releases are frozen so other projects can pin one.</p><picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <picture><img src="https://img.shields.io/badge/Parquet-1f3354?style=flat-square&logo=apacheparquet&logoColor=white" alt="Parquet"></picture> <a href="https://github.com/loggger101/AsteroidCatalog/releases/latest"><img src="https://img.shields.io/github/v/release/loggger101/AsteroidCatalog?style=flat-square&label=release&labelColor=1f3354&color=5ba3dc" alt="Latest release"></a> <a href="https://www.loganmedwardsastrophy.com/asteroid-catalog.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/spacecost">spacecost</a></b><br/><sub>Stage 3: mission costs</sub><br/><sub>8,725 lines of code</sub><br/><sub>17,478 total lines</sub><br/><picture><img src="docs/sparks/spacecost.svg" width="120" alt="My commits to spacecost each week since September 2026"></picture></td>
    <td valign="top"><p>The pipeline's mission-cost stage as an installable Python package: reference tables for mission cost and mass, with a citation on every row.</p><picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <picture><img src="https://img.shields.io/badge/pandas-1f3354?style=flat-square&logo=pandas&logoColor=white" alt="pandas"></picture> <a href="https://github.com/loggger101/spacecost/releases/latest"><img src="https://img.shields.io/github/v/release/loggger101/spacecost?style=flat-square&label=release&labelColor=1f3354&color=5ba3dc" alt="Latest release"></a> <a href="https://www.loganmedwardsastrophy.com/spacecost.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/General_Research">General_Research</a></b><br/><sub>the sources</sub><br/><sub>2,531 lines of code</sub><br/><sub>48,602 total lines</sub><br/><picture><img src="docs/sparks/General_Research.svg" width="120" alt="My commits to General_Research each week since September 2026"></picture></td>
    <td valign="top"><p>The sources behind the three repos above, ranked into tiers by authority, with the numbers I use pulled into a CSV for each source.</p><a href="https://www.loganmedwardsastrophy.com/general-research.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/starred-repos">starred-repos</a></b><br/><sub>pipeline audit</sub><br/><sub>705 lines of code</sub><br/><sub>2,528 total lines</sub><br/><picture><img src="docs/sparks/starred-repos.svg" width="120" alt="My commits to starred-repos each week since September 2026"></picture></td>
    <td valign="top"><p>An audit of 17 repos I'd starred, read for code and data the pipeline could use. Its probe scripts check economicspace's delta-v estimates against JPL's NHATS and against optimized Lambert transfers, and found two errors that partly cancel: the plane change is overcharged, and the transfer geometry undercharged by more.</p><picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <picture><img src="https://img.shields.io/badge/NumPy-1f3354?style=flat-square&logo=numpy&logoColor=white" alt="NumPy"></picture> <picture><img src="https://img.shields.io/badge/pandas-1f3354?style=flat-square&logo=pandas&logoColor=white" alt="pandas"></picture></td>
  </tr>
</table>

**Where it stands.** One row for each place the pipeline can deliver to, from its latest full-catalog runs: what the best mission costs for each dollar its cargo earns (filled dot) and what the median asteroid's does (open dot). Left of the dashed line, a mission pays for itself; none does yet.

<p align="center">
  <picture><source media="(max-width: 600px)" srcset="docs/breakeven-compact.svg"><img src="docs/breakeven.svg" width="100%" alt="Where the asteroid-mining pipeline stands: no destination breaks even yet. Cost per dollar earned, best mission and median asteroid, from economicspace's latest full-catalog runs: Mars surface 1.09× (2015 DS (X)), median 2.02×; Lunar surface 2.94× (2005 QP87 (X)), median 8.25×; Mars orbit 4.59× (350751 (B)), median 13.9×; Cislunar 4.84× (2018 DT (M)), median 20.9×; GEO 6.86× (2016 GS2 (D)), median 93.0×; LEO 17.0× (2005 QP87 (X)), median 60.5×; Earth surface 6,154× (2018 DT (M)), median 24,301×."></picture>
</p>

### <picture><img src="docs/icons/planetary.svg" width="24" height="24" align="top" alt=""></picture> Planetary science

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/asteroid-belt-gradient">asteroid-belt-gradient</a></b><br/><sub>paper and code</sub><br/><sub>2,862 lines of code</sub><br/><sub>6,529 total lines</sub><br/><picture><img src="docs/sparks/asteroid-belt-gradient.svg" width="120" alt="My commits to asteroid-belt-gradient each week since September 2026"></picture></td>
    <td valign="top"><p>Code and paper for <i>Constraints on the Origin of the Asteroid Belt's Compositional Gradient from Debiased Taxonomic Data</i>. It tests whether the belt's switch from S-types to C-types dates back to formation, using 161,659 classified asteroids from AsteroidCatalog after collapsing collisional families and correcting for the brightness bias that favors S-types. The code rebuilds every figure and number in the paper from two public input files.</p><picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <picture><img src="https://img.shields.io/badge/SciPy-1f3354?style=flat-square&logo=scipy&logoColor=white" alt="SciPy"></picture> <picture><img src="https://img.shields.io/badge/LaTeX-1f3354?style=flat-square&logo=latex&logoColor=white" alt="LaTeX"></picture> <a href="https://github.com/loggger101/asteroid-belt-gradient/releases/latest"><img src="https://img.shields.io/github/v/release/loggger101/asteroid-belt-gradient?style=flat-square&label=release&labelColor=1f3354&color=5ba3dc" alt="Latest release"></a> <a href="https://github.com/loggger101/asteroid-belt-gradient/tree/main/paper"><img src="https://img.shields.io/badge/Paper-AASTeX-5ba3dc?style=flat-square&labelColor=1f3354&logo=latex&logoColor=white" alt="Paper"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data">Mars Global Mosaic</a></b><br/><sub>Mars GIS mapping</sub><br/><sub>18,769 lines of code</sub><br/><sub>111,708 total lines</sub><br/><picture><img src="docs/sparks/Mars_Terrestrial_GlobalMosaic_GIS-Data.svg" width="120" alt="My commits to Mars Global Mosaic each week since October 2026"></picture></td>
    <td valign="top"><p>My project for OCN 4704 (Remote Sensing). In ArcGIS Pro I lined up Viking color, THEMIS day and night infrared, and HRSC/MOLA elevation between 60°N and 60°S to map lava flows, river channels and impact craters. A support vector machine classifies the landforms across that whole band, scoring 73.8% on areas it never trained on, and I've since trained RetinaNet and U-Net models to compare against it.</p><picture><img src="https://img.shields.io/badge/ArcGIS_Pro-1f3354?style=flat-square&logo=arcgis&logoColor=white" alt="ArcGIS Pro"></picture> <picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <a href="https://github.com/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data/releases/latest"><img src="https://img.shields.io/github/v/release/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data?style=flat-square&label=release&labelColor=1f3354&color=5ba3dc" alt="Latest release"></a></td>
  </tr>
</table>

### <picture><img src="docs/icons/learning.svg" width="24" height="24" align="top" alt=""></picture> Deep learning

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/star-spectral-classifier">star-spectral-classifier</a></b><br/><sub>stellar classification</sub><br/><sub>2,946 lines of code</sub><br/><sub>7,333 total lines</sub><br/><picture><img src="docs/sparks/star-spectral-classifier.svg" width="120" alt="My commits to star-spectral-classifier each week since September 2026"></picture></td>
    <td valign="top"><p>A multi-task CNN that predicts a star's Morgan-Keenan spectral letter and subclass digit from Pan-STARRS color cutouts, without any spectra. On 14k held-out cutouts it gets the letter right 84.3% of the time, and 98.4% within its top two guesses. Finished October 2025.</p><picture><img src="https://img.shields.io/badge/TensorFlow-1f3354?style=flat-square&logo=tensorflow&logoColor=white" alt="TensorFlow"></picture> <picture><img src="https://img.shields.io/badge/Astropy-1f3354?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPG1hc2sgaWQ9ImQiPjxyZWN0IHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0iI2ZmZiIvPjxwYXRoIGQ9Ik0xLjYyIDE2LjJBMTEuMiA0IC0yMiAwIDAgMjIuMzggNy44IiBmaWxsPSJub25lIiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMy44Ii8%2BPC9tYXNrPgo8bWFzayBpZD0iYiI%2BPHJlY3Qgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiBmaWxsPSIjZmZmIi8%2BPGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iNy42IiBmaWxsPSIjMDAwIi8%2BPC9tYXNrPgo8Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSI2LjQiIGZpbGw9IiNmZmYiIG1hc2s9InVybCgjZCkiLz4KPHBhdGggZD0iTTEuNjIgMTYuMkExMS4yIDQgLTIyIDAgMCAyMi4zOCA3LjgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjgiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNMS42MiAxNi4yQTExLjIgNCAtMjIgMCAxIDIyLjM4IDcuOCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjEuOCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBtYXNrPSJ1cmwoI2IpIi8%2BPC9zdmc%2B" alt="Astropy"></picture> <a href="https://www.kaggle.com/datasets/loggger/star-image-bundles"><img src="https://img.shields.io/badge/Dataset-Kaggle-5ba3dc?style=flat-square&logo=kaggle&logoColor=white&labelColor=1f3354" alt="Kaggle dataset"></a> <a href="https://www.loganmedwardsastrophy.com/star-catalog.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/drone-target-id">drone-target-id</a></b><br/><sub>aerial target ID</sub><br/><sub>1,509 lines of code</sub><br/><sub>4,779 total lines</sub><br/><picture><img src="docs/sparks/drone-target-id.svg" width="120" alt="My commits to drone-target-id each week since September 2026"></picture></td>
    <td valign="top"><p>YOLO finds and segments targets in aerial footage, then a multi-output CNN gives each one a fine class and a valid/invalid call. On a 27k held-out test set it scores 87.1% on fine class and 91.3% on valid/invalid. Finished December 2025.</p><picture><img src="https://img.shields.io/badge/TensorFlow-1f3354?style=flat-square&logo=tensorflow&logoColor=white" alt="TensorFlow"></picture> <picture><img src="https://img.shields.io/badge/YOLO-1f3354?style=flat-square&logo=ultralytics&logoColor=white" alt="YOLO"></picture> <picture><img src="https://img.shields.io/badge/OpenCV-1f3354?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV"></picture> <a href="https://www.kaggle.com/datasets/loggger/fpv-images"><img src="https://img.shields.io/badge/Dataset-Kaggle-5ba3dc?style=flat-square&logo=kaggle&logoColor=white&labelColor=1f3354" alt="Kaggle dataset"></a> <a href="https://www.loganmedwardsastrophy.com/drone-target.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
</table>

### <picture><img src="docs/icons/simulation.svg" width="24" height="24" align="top" alt=""></picture> Simulation

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/Satellite-Space-Flight">Satellite-Space-Flight</a></b><br/><sub>orbit simulator</sub><br/><sub>12,796 lines of code</sub><br/><sub>22,010 total lines</sub><br/><picture><img src="docs/sparks/Satellite-Space-Flight.svg" width="120" alt="My commits to Satellite-Space-Flight each week since September 2026"></picture></td>
    <td valign="top"><p>A 3-D Earth orbit simulator in pure Python. The physics runs in numpy (J2 to J4 gravity, drag, Sun and Moon, solar radiation pressure, maneuvers) and pygame draws it. You can also fly a multi-stage rocket to orbit from anywhere on Earth, or from one of fifteen real launch complexes.</p><picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <picture><img src="https://img.shields.io/badge/NumPy-1f3354?style=flat-square&logo=numpy&logoColor=white" alt="NumPy"></picture> <picture><img src="https://img.shields.io/badge/pygame-1f3354?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2ZmZiIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNNyA2aDEwYTYgNiAwIDAgMSA1LjkgNC45bC45IDUuMmEzLjMgMy4zIDAgMCAxLTUuNiAyLjhMMTUuNiAxNi40SDguNGwtMi42IDIuNWEzLjMgMy4zIDAgMCAxLTUuNi0yLjhsLjktNS4yQTYgNiAwIDAgMSA3IDZaCk02IDguNnYxLjlINC4xdjIuMkg2djEuOWgyLjJ2LTEuOWgxLjl2LTIuMkg4LjJWOC42WgpNMTUuMDUgMTAuMmExLjM1IDEuMzUgMCAxIDAgMi43IDBhMS4zNSAxLjM1IDAgMSAwLTIuNyAwWgpNMTcuNDUgMTIuNmExLjM1IDEuMzUgMCAxIDAgMi43IDBhMS4zNSAxLjM1IDAgMSAwLTIuNyAwWiIvPjwvc3ZnPg%3D%3D" alt="pygame"></picture></td>
  </tr>
</table>

### <picture><img src="docs/icons/rare-disease.svg" width="24" height="24" align="top" alt=""></picture> Rare-disease work

Both repos are private, but the sites are public.

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://www.aspirecures.com">AspireCURES</a></b><br/><sub>CTO</sub><br/><sub>10,712 lines of code</sub><br/><sub>20,801 total lines</sub><br/><picture><img src="docs/sparks/aspirecures.svg" width="120" alt="My commits to AspireCURES each week since June 2026"></picture></td>
    <td valign="top"><p>AspireCURES connects patients with rare brain diseases such as CSF1R-ALSP to clinical trials, studies and specialists. Its site runs on Cloudflare Pages with serverless registration, and I've built a weekly research feed for its nine disease pages.</p><picture><img src="https://img.shields.io/badge/Cloudflare_Pages-1f3354?style=flat-square&logo=cloudflarepages&logoColor=white" alt="Cloudflare Pages"></picture> <a href="https://www.aspirecures.com"><img src="https://img.shields.io/badge/Live-5ba3dc?style=flat-square&logo=cloudflare&logoColor=white" alt="Live site"></a> <a href="https://www.loganmedwardsastrophy.com/aspire-cures.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://www.sistershopefoundation.org">Sisters Hope Foundation</a></b><br/><sub>VP, Database Management</sub><br/><sub>5,219 lines of code</sub><br/><sub>11,270 total lines</sub><br/><picture><img src="docs/sparks/SistersHopeFoundation.svg" width="120" alt="My commits to Sisters Hope Foundation each week since July 2026"></picture></td>
    <td valign="top"><p>Sisters Hope is a 501(c)(3) patient advocacy group for ALSP and CSF1R-related disorders. I moved their site off Squarespace and onto Cloudflare Pages.</p><picture><img src="https://img.shields.io/badge/Cloudflare_Pages-1f3354?style=flat-square&logo=cloudflarepages&logoColor=white" alt="Cloudflare Pages"></picture> <a href="https://www.sistershopefoundation.org"><img src="https://img.shields.io/badge/Live-5ba3dc?style=flat-square&logo=cloudflare&logoColor=white" alt="Live site"></a></td>
  </tr>
</table>

### <picture><img src="docs/icons/elsewhere.svg" width="24" height="24" align="top" alt=""></picture> Elsewhere

<!-- GitHub sizes each table to its content. Two of these descriptions are short, so the spacer image (1px tall, transparent) widens the table to match the others; on phones it shrinks to nothing. -->
<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/website">website</a></b><br/><sub>portfolio site</sub><br/><sub>7,615 lines of code</sub><br/><sub>10,124 total lines</sub><br/><picture><img src="docs/sparks/website.svg" width="120" alt="My commits to website each week since November 2025"></picture></td>
    <td valign="top"><p>The code for my portfolio site. Plain HTML, CSS and JavaScript with no build step.</p><picture><img src="https://img.shields.io/badge/HTML5-1f3354?style=flat-square&logo=html5&logoColor=white" alt="HTML5"></picture> <picture><img src="https://img.shields.io/badge/CSS-1f3354?style=flat-square&logo=css&logoColor=white" alt="CSS"></picture> <picture><img src="https://img.shields.io/badge/JavaScript-1f3354?style=flat-square&logo=javascript&logoColor=white" alt="JavaScript"></picture> <a href="https://www.loganmedwardsastrophy.com/"><img src="https://img.shields.io/badge/Live-5ba3dc?style=flat-square&logo=github&logoColor=white" alt="Live site"></a> <a href="https://www.loganmedwardsastrophy.com/portfolio-website.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a><br/><picture><img src="docs/spacer.svg" width="2000" height="1" alt=""></picture></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/quietlaunch">quietlaunch</a></b><br/><sub>Streamlit launcher</sub><br/><sub>1,077 lines of code</sub><br/><sub>2,202 total lines</sub><br/><picture><img src="docs/sparks/quietlaunch.svg" width="120" alt="My commits to quietlaunch each week since August 2026"></picture></td>
    <td valign="top"><p>Starts a Streamlit app with no console window. A small control window shows the server booting, and why it failed if it does, opens the browser once the port answers, and stops the server and its children when closed. I split it out of economicspace's dashboard launcher; it uses only the standard library and is tested on Windows, Linux and macOS.</p><picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <picture><img src="https://img.shields.io/badge/Streamlit-1f3354?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"></picture> <a href="https://github.com/loggger101/quietlaunch/releases/latest"><img src="https://img.shields.io/github/v/release/loggger101/quietlaunch?style=flat-square&label=release&labelColor=1f3354&color=5ba3dc" alt="Latest release"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/quietqueue">quietqueue</a></b><br/><sub>unattended job queue</sub><br/><sub>646 lines of code</sub><br/><sub>1,589 total lines</sub><br/><picture><img src="docs/sparks/quietqueue.svg" width="120" alt="My commits to quietqueue each week since August 2026"></picture></td>
    <td valign="top"><p>Runs a queue of long jobs unattended on Windows and keeps it alive through a closed shell, a stray Ctrl+C, a reboot or a second copy started at logon. Each job is one subprocess, a ledger records what's finished so a restart picks up where it stopped, and the whole process tree can be paused and resumed without losing the job in flight. I split it out of economicspace's campaign runner, which ran a 28-job model campaign over several days.</p><picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <a href="https://github.com/loggger101/quietqueue/releases/latest"><img src="https://img.shields.io/github/v/release/loggger101/quietqueue?style=flat-square&label=release&labelColor=1f3354&color=5ba3dc" alt="Latest release"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/Hermes_Skills">Hermes_Skills</a></b><br/><sub>agent skills</sub><br/><picture><img src="docs/sparks/Hermes_Skills.svg" width="120" alt="My commits to Hermes_Skills each week since August 2026"></picture></td>
    <td valign="top"><p>My library of 253 agent skills in 23 categories, built for my Hermes agent setup.</p><picture><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></picture> <picture><img src="https://img.shields.io/badge/Markdown-1f3354?style=flat-square&logo=markdown&logoColor=white" alt="Markdown"></picture></td>
  </tr>
</table>

### <picture><img src="docs/icons/activity.svg" width="24" height="24" align="top" alt=""></picture> Every commit so far

Every commit I've made to the repos above, from the first to this week. Each ring is one section of this page, the outermost the first; time runs clockwise from twelve o'clock, and a bigger dot is a busier week. Bots' commits aren't counted.

<p align="center">
  <picture><source media="(max-width: 600px)" srcset="docs/activity-compact.svg"><img src="docs/activity.svg" width="100%" alt="Every commit I've made to these repos, from the first on 23 Nov 2025 to 24 Oct 2026, drawn as one orbit per section of this page: 3,153 in all, Space economics 609, Planetary science 119, Deep learning 15, Simulation 65, Rare-disease work 491, Elsewhere 1,854. Busiest week: 346 commits, the week of 5 Oct 2026. Latest: Mars Global Mosaic, 23 Oct 2026."></picture>
</p>

My latest commits:

<!-- latest commits -->
- 23 Oct · [Mars Global Mosaic](https://github.com/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data/commit/cdac6d75d9f4f2c7d8f7766468186a8d484d9019): The label proposals built on the drive: 1,086 rows, the laptop's result exactly
- 23 Oct · [Mars Global Mosaic](https://github.com/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data/commit/e11642d6741d03d4b351e48535689d411ade6eda): The final started: AASTeX paper and final deck, and the drive merged with §68
- 22 Oct · [General_Research](https://github.com/loggger101/General_Research/commit/f846ef86da9911b955c29117d23acb1a65e7b8d9): Round 240: owner rejects 8 sources; new "Sources to replace" list with 15 flags
- 22 Oct · [General_Research](https://github.com/loggger101/General_Research/commit/5418e8879a66ad91b9d3eda61258a634b000619d): Round 239: source audit; owner rejects 25 sources that back no cell or that upstream stopped citing
- 21 Oct · [starred-repos](https://github.com/loggger101/starred-repos/commit/223bfef746d4e9c5fdf37552f9b0268d61be9991): README: economicspace's orbital.py keeps only elements\_to\_state; the solvers are here alone
- 21 Oct · [spacecost](https://github.com/loggger101/spacecost/commit/643a7832ddcfd99eecc202ebfa2c36b7e8b175e6): Cut 0.12.6: seven wording and citation RCs (data contract 1.23.6)
<!-- /latest commits -->

### <picture><img src="docs/icons/languages.svg" width="24" height="24" align="top" alt=""></picture> Languages

The lines of code under each repo's name, added up by language.

<p align="center">
  <picture><source media="(max-width: 600px)" srcset="docs/languages-compact.svg"><img src="docs/languages.svg" width="100%" alt="107,081 lines of code in 10 languages: Python 87,162 (81.4%), Perl 6,747 (6.3%), JavaScript 5,326 (5.0%), HTML 4,092 (3.8%), CSS 2,375 (2.2%), Shell 644 (0.6%), Batchfile, PowerShell, VBScript and Dockerfile 735 (0.7%)."></picture>
</p>

### <picture><img src="docs/icons/flybys.svg" width="24" height="24" align="top" alt=""></picture> Passing Earth this week

The asteroids coming within 20 lunar distances of Earth in the week ahead, from NASA/JPL's close-approach data, refreshed every Monday. The sizes are estimates from each body's brightness, as almost none has been measured.

<p align="center">
  <picture><source media="(max-width: 600px)" srcset="docs/flybys-compact.svg"><img src="docs/flybys.svg" width="100%" alt="Asteroids passing Earth within 20 lunar distances, 24–30 Oct 2026 (NASA/JPL close-approach data): 9 in all. 2026 TB94, 5.1 lunar distances on Tue 27 Oct, 20–45 m, 11.6 km/s; 2026 UE, 5.2 lunar distances on Sun 25 Oct, 19–42 m, 15.9 km/s; 2026 SQ31, 6.0 lunar distances on Sun 25 Oct, 47–105 m, 7.8 km/s; 2026 TB8, 7.1 lunar distances on Sun 25 Oct, 45–100 m, 7.8 km/s; 2026 UB1, 9.5 lunar distances on Wed 28 Oct, 31–69 m, 18.7 km/s; 2018 GS1, 11.0 lunar distances on Wed 28 Oct, 81–180 m, 9.3 km/s; 2026 UD, 11.6 lunar distances on Fri 30 Oct, 20–44 m, 7.7 km/s; 2026 TT3, 12.8 lunar distances on Sat 24 Oct, 35–79 m, 12.8 km/s."></picture>
</p>

### <picture><img src="docs/icons/contact.svg" width="24" height="24" align="top" alt=""></picture> Get in touch

<p align="center">The contact form on my site goes straight to my email, or you can message me on LinkedIn.</p>

<p align="center">
  <a href="https://www.loganmedwardsastrophy.com/#contact"><img src="docs/links/contact.svg" height="36" alt="Contact form on loganmedwardsastrophy.com"></a>
  <a href="https://www.linkedin.com/in/logan-edwards-shf/"><img src="docs/links/linkedin.svg" height="36" alt="LinkedIn: logan-edwards"></a>
</p>

<p align="center"><sub>The charts, counts and cards on this page are drawn by Python scripts from the repos' own data, and most of them refresh every Monday. <a href="https://github.com/loggger101/Loggger101/tree/main/tools">See how they're made</a>.</sub></p>

<br/>
<p align="center"><picture><source media="(max-width: 600px)" srcset="docs/footer-compact.svg"><img src="docs/footer.svg" width="100%" alt=""></picture></p>
