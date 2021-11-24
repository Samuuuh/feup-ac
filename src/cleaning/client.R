# Executed inside src/cleaning folder

# Must import the preprocessed/client.csv
client<-read.delim("../data/preprocessed/client.csv", sep=";")

client$birthdate <- NULL

# Sex from categorical to numerical.
client$sex<-unclass(as.factor(client$sex))

write.csv(client, file="../data/cleaned/client.csv", row.names = FALSE)
