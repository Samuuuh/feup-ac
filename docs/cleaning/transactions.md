# 1) Transactions missing data

As we have seem in the data exploration, we have many null values in this table.



![](https://i.imgur.com/33IdTAJ.png)

Our approach will be consisted in checking if it's worthy treating the data. 

- If yes, we treat it.
- Case not we drop the column. In this case the treating will not provide any good to our  models. 

## Operation

As we can see we have 70761 NaN values. 

![](https://i.imgur.com/zpLcjmZ.png)	



Firstly, does it make sense to treat this variable?  Let's check how it's related to the status:

```R
merged %>%
  group_by(operation) %>% 
  count(status)
```

```r
# A tibble: 7 x 3
# Groups:   operation [4]
  operation    status     n
  <chr>         <int> <int>
1 another bank     -1   211
2 another bank      1  3961
3 cash             -1  2155
4 cash              1 13813
5 credit card       1    23
6 nan              -1   604
7 nan               1  3727
```

We have interesting data here... All the people that have maid any transaction in credit card contains a status equals to 1. We can create other types of features from this in the future. 

The number of NaN elements here is __enough to build another categorical variable__, since there're many types of operations a person may do. 

```r
trans$operation[trans$operation == "nan"]<-"other"
```

![](https://i.imgur.com/ysEEm4Z.png)

Conclusion: __Another variable should be created__. 



## k_symbol

We have a lot of NaN values here:

![image-20211125112643996](C:\Users\julia\AppData\Roaming\Typora\typora-user-images\image-20211125112643996.png)

Let's once again check if the k_symbol is somehow important. 

```r
merged %>%
  group_by(k_symbol) %>% 
  count(status)
```

```
# A tibble: 6 x 3
   k_symbol                                status    perc
   <chr>                                    <int> <float>
 1 ""                                          -1  0.1207
 2 "household"                                 -1  0.0777
 3 "insurrance payment"                        -1  0.0596
 4 "interest credited"                         -1  0.1394
 5 "payment for statement"                     -1  0.1246
 6 "sanction interest if negative balance"     -1  0.6842
```

As we may see the variables are not relevant except for the `"sanction interest if negative balance"`. 

Thus let's set the NaN values as another variable. 

Conclusion: __another variable should be created from this__. 



## Bank

The bank is not really a useful variable. 

![](https://i.imgur.com/U9ZYTsq.png)

The majority of the people does not have data about banks. 

Also, there isn't any other category that is highlighted among the others.

Conclusions: __should not be used__. 

## Account

Since this column contains a lot of missing data and inconsistent, this column should be dropped. The information isn't really that relevant, since they're just identification numbers.

![](https://i.imgur.com/MNeJOfV.png)



We have some missing data here. Let's set the __NaN__ values to zero as well. 

Some account_id's don't have any `account` associated. To check how this specific case may be related with the status, let's create another column which tells if our `account` value is undefined. 

```r
merged$is_na <-merged$account == 0
```

Now, let's make an `AND` operation, by using `min`. We gonna group the table by the `account_id` and `status` and get the `min` value of the `is_na` column, which is equivalent to an `AND`. 

```r
counter<-merged %>%
  group_by(account_id, status) %>%
  summarise(only_na_account=min(is_na))
```

Our table will look like this:

![](https://i.imgur.com/5rXIZQj.png)

The conclusion that get from this table is:

```r
# Groups:   only_na_account [2]
  only_na_account status     n
            <int>  <int> <int>
1               0     -1    14
2               0      1   211
3               1     -1    32
4               1      1    71
```

The people who doesn't have any account identification are much more likely to have a status 1. 

