library(dplyr)
library(ggplot2)
library(ggpubr)
library(RSQLite)
library(DBI)
source("./utils.R")

con <- dbConnect(RSQLite::SQLite(), "data/ac-dev_v-1.db")
dist <- dbGetQuery(con, "SELECT * FROM district")

# OUTLIERS ====================================================================
# we can see that the south region contains a outlier, with 100% of urban inhab.
names(dist)
show_all_outliers_plot(dist[c("num_inhab", "perc_unemploy_95")])
show_all_outliers_plot(dist[c("enterp_per_1000", "num_crimes_95")])
show_all_outliers_plot(dist[c("perc_urban_inhab", "num_cities")])

# MISSING DATA ===============================================================

# perc_unemploy_95 and num_crimes_95 columns contains missing data.

# We have missing data at the id = 69
columns<-colnames(dist)
filter_at(dist, vars(columns), any_vars(. == '?'))

dist_no_missing<-dist[dist$perc_unemploy_95 != '?', ]
dist_no_missing$perc_unemploy_95 = as.numeric(dist_no_missing$perc_unemploy_95)

ggplot(dist_no_missing, aes(sample=perc_unemploy_95)) + geom_qq(geom='point') +
  stat_qq_line()+ ggtitle("QQPlot for perc_unemploy_95")

ggdensity(dist_no_missing$perc_unemploy_95, main="Density of unemployed in 95")


# FEATURE SELECTION ===========================================================


# The variables are very correlated. So, we gonna drop the perc_unemploy_95
cor.test(dist_no_missing$perc_unemploy_95, dist_no_missing$perc_unemploy_96, method="pearson")

# num_crimes_95
dist_no_missing$num_crimes_95 = as.numeric(dist_no_missing$num_crimes_95)
cor.test(dist_no_missing$num_crimes_95, dist_no_missing$num_crimes_96, method="pearson")

# Let's drop the rows of the year 95, since they are redundant.
dist$num_crimes_95<-NULL
dist$perc_unemploy_95<-NULL
dist$num_municip_inhab_0_499 <- NULL
dist$num_municip_inhab_0_499 <- NULL
dist$num_municip_inhab_500_1999 <- NULL
dist$num_municip_inhab_2000_9999 <- NULL
dist$num_municip_inhab_10000_  <- NULL
dist$num_cities  <- NULL

# Categorical data to numeric.
dist_factor_region <- factor(dist$region)
dist$region <- unclass(dist_factor_region)
dist

# Numeric data
write.csv(dist, file="data/cleaned/dist.csv", row.names = FALSE)
