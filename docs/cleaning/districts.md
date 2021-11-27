## Districts

__LIBRARIES USED__
```r=
library(dplyr)
library(ggplot2)
```

__IMPORTING DATA__
```r=
dist<-read.delim("../data/preprocessed/district.csv", sep=";")
```

__OUTLIERS__
We searched for some outliers in the percentage of urban inhabitants.

![](https://i.imgur.com/ua2gK02.png)


As we can see the prague region contains 100% of inhabitants, but we can't actually drop this region, since many clients comes from it. 

Let's keep in mind the that Prague and some cities in Moravia contains high number of urban inhabitants.


__MISSING DATA__
We have some missing data at `perc_unemploy_95` and `num_crimes_95`

```r=
# We have missing data at the id = 69
columns<-colnames(dist)
filter_at(dist, vars(columns), any_vars(. == '?'))
```

- Treating `perc_unemploy_95`. Let's check if it follows a normal distribution:

![](https://i.imgur.com/XIOIe6k.png)

Still checking the density:

![](https://i.imgur.com/JAR0JmO.png)

Not really similar to a normal distribution...





__FEATURE SELECTION__

By doing the `Pearson's product-moment correlation`, we can see that `perc_unemploy_95` and `perc_unemploy_96` are strongly correlated. Thus, we may want to drop the `perc_unemploy_95`. 

```r=
dist_no_missing<-dist[dist$perc_unemploy_95 != '?', ]
dist_no_missing$perc_unemploy_95 = as.numeric(dist_no_missing$perc_unemploy_95)

# The variables are very correlated. So, we gonna drop the perc_unemploy_95
cor.test(dist_no_missing$perc_unemploy_95, dist_no_missing$perc_unemploy_96, method="pearson")
```
```
data:  dist_no_missing$perc_unemploy_95 and dist_no_missing$perc_unemploy_96
t = 41.57, df = 70, p-value < 2.2e-16
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 0.9686717 0.9876910
sample estimates:
      cor 
0.9803411 
```
