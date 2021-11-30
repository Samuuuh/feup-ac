

disp <- read.delim("../../data/preprocessed/disp.csv", sep=";")

# Just use owners.
disp<-disp[disp$type == 'owner', ]
disp$type<-NULL

write.csv(disp, file="../../data/cleaned/disp.csv", row.names = FALSE)