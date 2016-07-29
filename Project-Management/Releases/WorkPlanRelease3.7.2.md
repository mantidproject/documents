# Mantid Patch Release 3.7.2


## Issues and PRs whcih were marked for this Patch Release


| Owner  | Patch PR             | Link to test description | Has passed test?| On `release-v3.7`
|--------|----------------------|--------------------------|-----------------|-----|
|Anton   | [load cansas data without idev](https://github.com/mantidproject/mantid/pull/17005)||| <li>[x]</li>
|Martyn  | [Register VSI usage with UsageService](https://github.com/mantidproject/mantid/pull/16946)|||<li>[x]</li>|
|Stuart  |[Update VisionReduction to import string explicitly](https://github.com/mantidproject/mantid/pull/16988) |||<li>[x]</li> |
| Stuart |[Update VisionReduction.py ](https://github.com/mantidproject/mantid/pull/16974)|||<li>[x]</li>|
| Andrei  | [New CNCS definition](https://github.com/mantidproject/mantid/pull/16933) |||<li>[x]</li>|  
| Peter   | [Update live data urls for ADARA beamlines](https://github.com/mantidproject/mantid/pull/16906)|||<li>[x]</li>|  
| Anton   | [Correct process note in SaveCanSAS1D](https://github.com/mantidproject/mantid/pull/16900)|||<li>[x]</li>|  
| Vickie  | [New IDF for TOPAZ](https://github.com/mantidproject/mantid/pull/16898)|||<li>[x]</li>|
| Anton   | [Fix LoadRKH for data with second header and 2D data](https://github.com/mantidproject/mantid/pull/16884) |||<li>[x]</li>|  
| Anton   | [ISIS SANS improvements to batch processing and beam centre finder ](https://github.com/mantidproject/mantid/pull/16875)|||<li>[x]</li>|
| Anton   | [Fix larmor loading multiperiod event data](https://github.com/mantidproject/mantid/pull/16791)|||<li>[x]</li>|  
| Anton   | [Fix beam center finder masking in ISIS SANS](https://github.com/mantidproject/mantid/pull/16764)|||<li>[x]</li>|  
| Vickie  | [16539 mpi algorithms dont compile ](https://github.com/mantidproject/mantid/pull/16641)|||<li>[x]</li>|  
| Nick    | [Add usage tracking for interfaces ](https://github.com/mantidproject/mantid/pull/16594)|||<li>[x]</li>|  



## Test Plan

### Test descriptions

* **load cansas data without idev**
  * This item will be review by the ISIS SANS group.
* **Fix LoadRKH for data with second header and 2D data**
  * This item will be review by the ISIS SANS group.
* **Fix larmor loading multiperiod event data**
  * This item will be review by the ISIS SANS group.
* **n	Fix beam center finder masking in ISIS SANS**
  * This item will be review by the ISIS SANS group.
* **ISIS SANS improvements to batch processing and beam centre finder**
  * This item will be review by the ISIS SANS group.



## Work pipeline

- [x] Steven and Peter cherry-picked most of the commits from the SNS onto `release-v3.7`
- [x] Cherry-picked ISIS commits onto `release-v3.7` + PR *16539 mpi algorithms dont compile*
- [x] Double check that commits of PRs are present on `release-v3.7`
- [x] Add to relese notes for 3.7.2
- [x] Create an installer, perform broad tests
- [x] Push to release pipeline
- [ ] Provide ISIS SANS scientists with Windows installers for testing
- [ ] ...
