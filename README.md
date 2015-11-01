# flexindex

# TODO
* Batch generation of offers/models
* Use full-weight version of report-data files: categories.xml, etc

# DEPENDENCIES
* Offer -> Hyper Category
* Offer -> Outlet
* Offer -> Model
* Offer -> GLParams
* Model -> ModelStat
* ModelStat -> Region
* Shop -> Region
* Outlet -> Shop
* Hyper Category -> Navigation Category
* GLParams -> GLMbo

# KNOWN ISSUES
* Non-sync statistics -- in doubt for usability

# PHILOSOPHY
* All autogeneration is made on save stage, not earlier, if it can influence other objects
