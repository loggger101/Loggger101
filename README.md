<p align="center">
  <a href="https://www.loganmedwardsastrophy.com/"><img src="docs/banner.svg" width="100%" alt="Logan M Edwards, Astronomy and Astrophysics, Planetary Science"></a>
  <br/>
  <a href="https://github.com/loggger101"><img src="docs/typing.svg" width="482" alt="Asteroid catalogs and mining economics. Asteroid belt origins and Mars mapping. Deep learning on survey imagery. Orbit simulation in pure Python."></a>
  <br/>
  <a href="https://www.loganmedwardsastrophy.com/"><img src="docs/links/website.svg" height="36" alt="Website: loganmedwardsastrophy.com"></a>
  <a href="https://www.loganmedwardsastrophy.com/Logan_Edwards_CV.pdf"><img src="docs/links/cv.svg" height="36" alt="CV (PDF)"></a>
  <a href="https://www.linkedin.com/in/logan-edwards-shf/"><img src="docs/links/linkedin.svg" height="36" alt="LinkedIn: logan-edwards"></a>
  <a href="https://www.kaggle.com/loggger"><img src="docs/links/kaggle.svg" height="36" alt="Kaggle: loggger"></a>
</p>

I'm an Astronomy & Astrophysics student at Florida Tech, double majoring in Planetary Science. Most of the work here is about asteroids. I built a catalog of about 1.57 million of them and a pipeline that estimates whether mining one would make money, then used the catalog for a [paper](https://github.com/loggger101/asteroid-belt-gradient) on whether the belt's S/C composition gradient is left over from when the planets formed. I've also trained two image classifiers and written an orbit simulator.

Outside of school I'm CTO of [AspireCURES](https://www.aspirecures.com), a company that matches patients with rare brain diseases to research, and VP of Database Management at [Sisters Hope Foundation](https://www.sistershopefoundation.org), a rare-disease nonprofit. I run the websites and patient databases for both.

<p align="center">
  <a href="https://github.com/loggger101/AsteroidCatalog"><picture><source media="(max-width: 600px)" srcset="docs/stats/catalog-compact.svg"><img src="docs/stats/catalog.svg" width="23.5%" alt="1.57M asteroids cataloged (AsteroidCatalog)"></picture></a>
  <a href="https://github.com/loggger101/asteroid-belt-gradient"><picture><source media="(max-width: 600px)" srcset="docs/stats/belt-compact.svg"><img src="docs/stats/belt.svg" width="23.5%" alt="161,659 classified asteroids analyzed (asteroid-belt-gradient)"></picture></a>
  <a href="https://github.com/loggger101/General_Research"><picture><source media="(max-width: 600px)" srcset="docs/stats/sources-compact.svg"><img src="docs/stats/sources.svg" width="23.5%" alt="574 research sources (General_Research)"></picture></a>
  <a href="https://github.com/loggger101/Hermes_Skills"><picture><source media="(max-width: 600px)" srcset="docs/stats/skills-compact.svg"><img src="docs/stats/skills.svg" width="23.5%" alt="253 agent skills (Hermes_Skills)"></picture></a>
</p>

<p align="center">
  <a href="https://github.com/loggger101/Satellite-Space-Flight"><picture><source media="(max-width: 600px)" srcset="docs/gallery/satellite-compact.webp"><img src="docs/gallery/satellite.webp" width="48.5%" alt="Satellite-Space-Flight: the ISS orbit, live elements and ground-station passes"></picture></a>
  <a href="https://github.com/loggger101/asteroid-belt-gradient"><picture><source media="(max-width: 600px)" srcset="docs/gallery/belt-compact.webp"><img src="docs/gallery/belt.webp" width="48.5%" alt="asteroid-belt-gradient: S-types give way to C-types farther from the Sun (fraction by number across semimajor axis, D of at least 53 km, families collapsed)"></picture></a>
  <a href="https://github.com/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data"><picture><source media="(max-width: 600px)" srcset="docs/gallery/mars-compact.webp"><img src="docs/gallery/mars.webp" width="48.5%" alt="Mars Global Mosaic: SVM landform classes across Tharsis and Valles Marineris"></picture></a>
  <a href="https://github.com/loggger101/drone-target-id"><picture><source media="(max-width: 600px)" srcset="docs/gallery/drone-compact.webp"><img src="docs/gallery/drone.webp" width="48.5%" alt="drone-target-id: per-target valid/invalid scores on aerial footage"></picture></a>
</p>

### <img src="docs/icons/economics.svg" width="24" height="24" align="top" alt=""> Space economics

These four repos work together to estimate whether an uncrewed asteroid mining mission would turn a profit. The catalog also feeds my paper.

<p align="center">
  <picture><source media="(max-width: 600px)" srcset="docs/pipeline-compact.svg"><img src="docs/pipeline.svg" width="100%" alt="How the repos connect: General_Research holds the sources that AsteroidCatalog, spacecost and economicspace cite. AsteroidCatalog releases feed asteroid-belt-gradient, which builds the paper, and economicspace, which also installs spacecost and ranks mining targets by profit."></picture>
</p>

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/economicspace">economicspace</a></b><br/><sub>the pipeline</sub><br/><sub>22,606 lines of code</sub></td>
    <td valign="top"><p>The main pipeline. It builds a catalog from public astronomy databases, prices the minerals, costs the transport, then runs the rocket equation and a cost cascade to rank targets by profit.</p><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/pandas-1f3354?style=flat-square&logo=pandas&logoColor=white" alt="pandas"> <img src="https://img.shields.io/badge/Docker-1f3354?style=flat-square&logo=docker&logoColor=white" alt="Docker"></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/AsteroidCatalog">AsteroidCatalog</a></b><br/><sub>Stage 1: the catalog</sub><br/><sub>5,609 lines of code</sub></td>
    <td valign="top"><p>The pipeline's catalog stage, moved into its own repo. About 1.57 million asteroids from JPL SBDB, SsODNet, NEOWISE and MP3C, cross-matched, with the source of every value recorded and a cited composition estimate for each taxonomy class. Releases are frozen so other projects can pin one.</p><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Parquet-1f3354?style=flat-square&logo=apacheparquet&logoColor=white" alt="Parquet"> <img src="https://img.shields.io/github/v/release/loggger101/AsteroidCatalog?style=flat-square&label=release&labelColor=1f3354&color=5ba3dc" alt="Latest release"> <a href="https://www.loganmedwardsastrophy.com/asteroid-catalog.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/spacecost">spacecost</a></b><br/><sub>Stage 3: mission costs</sub><br/><sub>8,311 lines of code</sub></td>
    <td valign="top"><p>The pipeline's mission-cost stage as an installable Python package: reference tables for mission cost and mass, with a citation on every row.</p><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/pandas-1f3354?style=flat-square&logo=pandas&logoColor=white" alt="pandas"> <img src="https://img.shields.io/github/v/release/loggger101/spacecost?style=flat-square&label=release&labelColor=1f3354&color=5ba3dc" alt="Latest release"> <a href="https://www.loganmedwardsastrophy.com/spacecost.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/General_Research">General_Research</a></b><br/><sub>the sources</sub><br/><sub>2,397 lines of code</sub></td>
    <td valign="top"><p>The sources behind the other three, ranked into tiers by authority, with the numbers I use pulled into a CSV for each source.</p><a href="https://www.loganmedwardsastrophy.com/general-research.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
</table>

### <img src="docs/icons/planetary.svg" width="24" height="24" align="top" alt=""> Planetary science

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/asteroid-belt-gradient">asteroid-belt-gradient</a></b><br/><sub>paper and code</sub><br/><sub>2,862 lines of code</sub></td>
    <td valign="top"><p>Code and paper for <i>Constraints on the Origin of the Asteroid Belt's Compositional Gradient from Debiased Taxonomic Data</i>. It tests whether the belt's switch from S-types to C-types dates back to formation, using 161,659 classified asteroids from AsteroidCatalog after collapsing collisional families and correcting for the brightness bias that favors S-types. The code rebuilds every figure and number in the paper from two public input files.</p><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/SciPy-1f3354?style=flat-square&logo=scipy&logoColor=white" alt="SciPy"> <img src="https://img.shields.io/badge/LaTeX-1f3354?style=flat-square&logo=latex&logoColor=white" alt="LaTeX"> <img src="https://img.shields.io/github/v/release/loggger101/asteroid-belt-gradient?style=flat-square&label=release&labelColor=1f3354&color=5ba3dc" alt="Latest release"> <a href="https://github.com/loggger101/asteroid-belt-gradient/tree/main/paper"><img src="https://img.shields.io/badge/Paper-AASTeX-5ba3dc?style=flat-square&labelColor=1f3354&logo=latex&logoColor=white" alt="Paper"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/Mars_Terrestrial_GlobalMosaic_GIS-Data">Mars Global Mosaic</a></b><br/><sub>Mars GIS mapping</sub><br/><sub>14,445 lines of code</sub></td>
    <td valign="top"><p>My project for OCN 4704 (Remote Sensing). In ArcGIS Pro I lined up Viking color, THEMIS day and night infrared, and HRSC/MOLA elevation between 60°N and 60°S, then mapped lava flows, river channels and impact craters.</p><img src="https://img.shields.io/badge/ArcGIS_Pro-1f3354?style=flat-square&logo=arcgis&logoColor=white" alt="ArcGIS Pro"> <img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"></td>
  </tr>
</table>

### <img src="docs/icons/learning.svg" width="24" height="24" align="top" alt=""> Deep learning

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/star-spectral-classifier">star-spectral-classifier</a></b><br/><sub>stellar classification</sub><br/><sub>2,946 lines of code</sub></td>
    <td valign="top"><p>A multi-task CNN that predicts a star's Morgan-Keenan spectral letter and subclass digit from Pan-STARRS color cutouts, without any spectra. On 14k held-out cutouts it gets the letter right 84.3% of the time, and 98.4% within its top two guesses. Finished 10/21/2025.</p><img src="https://img.shields.io/badge/TensorFlow-1f3354?style=flat-square&logo=tensorflow&logoColor=white" alt="TensorFlow"> <img src="https://img.shields.io/badge/Astropy-1f3354?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPG1hc2sgaWQ9ImQiPjxyZWN0IHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0iI2ZmZiIvPjxwYXRoIGQ9Ik0xLjYyIDE2LjJBMTEuMiA0IC0yMiAwIDAgMjIuMzggNy44IiBmaWxsPSJub25lIiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMy44Ii8%2BPC9tYXNrPgo8bWFzayBpZD0iYiI%2BPHJlY3Qgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiBmaWxsPSIjZmZmIi8%2BPGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iNy42IiBmaWxsPSIjMDAwIi8%2BPC9tYXNrPgo8Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSI2LjQiIGZpbGw9IiNmZmYiIG1hc2s9InVybCgjZCkiLz4KPHBhdGggZD0iTTEuNjIgMTYuMkExMS4yIDQgLTIyIDAgMCAyMi4zOCA3LjgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjgiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8cGF0aCBkPSJNMS42MiAxNi4yQTExLjIgNCAtMjIgMCAxIDIyLjM4IDcuOCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjEuOCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBtYXNrPSJ1cmwoI2IpIi8%2BPC9zdmc%2B" alt="Astropy"> <a href="https://www.kaggle.com/datasets/loggger/star-image-bundles"><img src="https://img.shields.io/badge/Dataset-Kaggle-5ba3dc?style=flat-square&logo=kaggle&logoColor=white&labelColor=1f3354" alt="Kaggle dataset"></a> <a href="https://www.loganmedwardsastrophy.com/star-catalog.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/drone-target-id">drone-target-id</a></b><br/><sub>aerial target ID</sub><br/><sub>1,509 lines of code</sub></td>
    <td valign="top"><p>YOLO finds and segments targets in aerial footage, then a multi-output CNN gives each one a fine class and a valid/invalid call. On a 27k held-out test set it scores 87.1% on fine class and 91.3% on valid/invalid. Finished 12/6/2025.</p><img src="https://img.shields.io/badge/TensorFlow-1f3354?style=flat-square&logo=tensorflow&logoColor=white" alt="TensorFlow"> <img src="https://img.shields.io/badge/YOLO-1f3354?style=flat-square&logo=ultralytics&logoColor=white" alt="YOLO"> <img src="https://img.shields.io/badge/OpenCV-1f3354?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV"> <a href="https://www.kaggle.com/datasets/loggger/fpv-images"><img src="https://img.shields.io/badge/Dataset-Kaggle-5ba3dc?style=flat-square&logo=kaggle&logoColor=white&labelColor=1f3354" alt="Kaggle dataset"></a> <a href="https://www.loganmedwardsastrophy.com/drone-target.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
</table>

### <img src="docs/icons/simulation.svg" width="24" height="24" align="top" alt=""> Simulation

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/Satellite-Space-Flight">Satellite-Space-Flight</a></b><br/><sub>orbit simulator</sub><br/><sub>12,796 lines of code</sub></td>
    <td valign="top"><p>A 3-D Earth orbit simulator in pure Python. The physics runs in numpy (J2 to J4 gravity, drag, Sun and Moon, solar radiation pressure, maneuvers) and pygame draws it. You can also fly a multi-stage rocket to orbit from anywhere on Earth, or from one of fifteen real launch complexes.</p><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/NumPy-1f3354?style=flat-square&logo=numpy&logoColor=white" alt="NumPy"> <img src="https://img.shields.io/badge/pygame-1f3354?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2ZmZiIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNNyA2aDEwYTYgNiAwIDAgMSA1LjkgNC45bC45IDUuMmEzLjMgMy4zIDAgMCAxLTUuNiAyLjhMMTUuNiAxNi40SDguNGwtMi42IDIuNWEzLjMgMy4zIDAgMCAxLTUuNi0yLjhsLjktNS4yQTYgNiAwIDAgMSA3IDZaCk02IDguNnYxLjlINC4xdjIuMkg2djEuOWgyLjJ2LTEuOWgxLjl2LTIuMkg4LjJWOC42WgpNMTUuMDUgMTAuMmExLjM1IDEuMzUgMCAxIDAgMi43IDBhMS4zNSAxLjM1IDAgMSAwLTIuNyAwWgpNMTcuNDUgMTIuNmExLjM1IDEuMzUgMCAxIDAgMi43IDBhMS4zNSAxLjM1IDAgMSAwLTIuNyAwWiIvPjwvc3ZnPg%3D%3D" alt="pygame"></td>
  </tr>
</table>

### <img src="docs/icons/rare-disease.svg" width="24" height="24" align="top" alt=""> Rare-disease work

Both repos are private, but the sites are public.

<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://www.aspirecures.com">AspireCURES</a></b><br/><sub>CTO</sub><br/><sub>9,961 lines of code</sub></td>
    <td valign="top"><p>AspireCURES connects patients with rare brain diseases such as CSF1R-ALSP to clinical trials, studies and specialists. Its site runs on Cloudflare Pages with serverless registration, and I've built a weekly research feed for its nine disease pages.</p><img src="https://img.shields.io/badge/Cloudflare_Pages-1f3354?style=flat-square&logo=cloudflarepages&logoColor=white" alt="Cloudflare Pages"> <a href="https://www.aspirecures.com"><img src="https://img.shields.io/badge/Live-5ba3dc?style=flat-square&logo=cloudflare&logoColor=white" alt="Live site"></a> <a href="https://www.loganmedwardsastrophy.com/aspire-cures.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://www.sistershopefoundation.org">Sisters Hope Foundation</a></b><br/><sub>VP, Database Management</sub><br/><sub>5,219 lines of code</sub></td>
    <td valign="top"><p>Sisters Hope is a 501(c)(3) patient advocacy group for ALSP and CSF1R-related disorders. I moved their site off Squarespace and onto Cloudflare Pages.</p><img src="https://img.shields.io/badge/Cloudflare_Pages-1f3354?style=flat-square&logo=cloudflarepages&logoColor=white" alt="Cloudflare Pages"> <a href="https://www.sistershopefoundation.org"><img src="https://img.shields.io/badge/Live-5ba3dc?style=flat-square&logo=cloudflare&logoColor=white" alt="Live site"></a></td>
  </tr>
</table>

### <img src="docs/icons/elsewhere.svg" width="24" height="24" align="top" alt=""> Elsewhere

<!-- GitHub sizes each table to its content. These two descriptions are short, so the spacer image (1px tall, transparent) widens the table to match the others; on phones it shrinks to nothing. -->
<table>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/website">website</a></b><br/><sub>portfolio site</sub><br/><sub>7,577 lines of code</sub></td>
    <td valign="top"><p>The code for my portfolio site. Plain HTML, CSS and JavaScript with no build step.</p><img src="https://img.shields.io/badge/HTML5-1f3354?style=flat-square&logo=html5&logoColor=white" alt="HTML5"> <img src="https://img.shields.io/badge/CSS-1f3354?style=flat-square&logo=css&logoColor=white" alt="CSS"> <img src="https://img.shields.io/badge/JavaScript-1f3354?style=flat-square&logo=javascript&logoColor=white" alt="JavaScript"> <a href="https://www.loganmedwardsastrophy.com/"><img src="https://img.shields.io/badge/Live-5ba3dc?style=flat-square&logo=github&logoColor=white" alt="Live site"></a> <a href="https://www.loganmedwardsastrophy.com/portfolio-website.html"><img src="https://img.shields.io/badge/Project_page-5ba3dc?style=flat-square&logo=googlechrome&logoColor=white" alt="Project page"></a><br/><img src="docs/spacer.svg" width="2000" height="1" alt=""></td>
  </tr>
  <tr>
    <td width="24%" valign="top"><b><a href="https://github.com/loggger101/Hermes_Skills">Hermes_Skills</a></b><br/><sub>agent skills</sub></td>
    <td valign="top"><p>My library of 253 agent skills in 23 categories, built for my Hermes agent setup.</p><img src="https://img.shields.io/badge/Python-1f3354?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Markdown-1f3354?style=flat-square&logo=markdown&logoColor=white" alt="Markdown"></td>
  </tr>
</table>

### <img src="docs/icons/contact.svg" width="24" height="24" align="top" alt=""> Get in touch

<p align="center">The contact form on my site goes straight to my email, or you can message me on LinkedIn.</p>

<p align="center">
  <a href="https://www.loganmedwardsastrophy.com/#contact"><img src="docs/links/contact.svg" height="36" alt="Contact form on loganmedwardsastrophy.com"></a>
  <a href="https://www.linkedin.com/in/logan-edwards-shf/"><img src="docs/links/linkedin.svg" height="36" alt="LinkedIn: logan-edwards"></a>
</p>

<br/>
<p align="center"><picture><source media="(max-width: 600px)" srcset="docs/footer-compact.svg"><img src="docs/footer.svg" width="100%" alt=""></picture></p>
