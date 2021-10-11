
# Pay attention: the column-name should be more easy to read or use lowercase. Avoid to use simple name may conflict with R language internal parameters
      
eol_ana <- read.csv("C:/Users/uib10158/Desktop/data_clean/ct_raw_data_clean_20211011/0_20211006_161139213_RawTarget_extract.csv")
View(eol_ana)
head(eol_ana)

library(tidyverse)
library(skimr)

eol_ana_dis <-filter(eol_ana, distance == 1.6)
View(eol_ana_dis)

eol_ana_dis %>% 
  group_by(Tx_Module) %>% 
  drop_na() %>% 
  summarize(max_angle=max(angle,na.rm = TRUE), 
            mean_angle=min(angle, na.rm=TRUE),
            sd_angle=sd(angle, na.rm=TRUE))

ggplot(data=eol_ana_dis)+
  geom_point(mapping=aes(x=distance, y=angle, color=Tx_Module))+facet_wrap(~Tx_Module)





