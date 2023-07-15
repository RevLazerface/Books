library(tidyverse)
library(here)
library(ggthemr)
library(shiny)

# Set visual theme for plot (don't know if this works for shiny)
ggthemr("dust")

# Get data from csv file
books_data <- read_csv(here("books_data.csv"))

# Generate new variables
books <- books_data %>% 
  mutate(Vocab_Rate = round(Total_Vocabulary/Total_Words, digits = 2),
        Total_WPS = round(Total_Words/Total_Sentences, digits = 2),
        Total_CPW = round(Total_Characters/Total_Words, digits = 2),
        First_CPW = round(FS_Characters/FS_Words, digits = 2),
        Last_CPW = round(LS_Characters/LS_Words, digits = 2),) 
  # %>% select(-c(Total_Characters, Total_Vocabulary, Total_Sentences, FS_Characters, LS_Characters))

# Create table from which to generate bar chart
plot_tab <- books %>% 
  select(c(Title, Author, Genre, Total_WPS, FS_Words, LS_Words, Vocab_Rate, Total_Words)) %>%
  rename('Total Average'='Total_WPS', 'First'='FS_Words', 'Last'='LS_Words', 'Vocab Rate'='Vocab_Rate', 'Word Count'='Total_Words') %>% 
  gather(key= 'Position', value= 'Length', 'Total Average':Last) %>% 
  arrange(Author, Title)%>% 
  separate_rows(Genre, sep=",") 

plot_tab$Genre <- gsub(" ", "", plot_tab$Genre)


# I think these both do the same thing, set the order of the groups/subgroups of bars
plot_tab$Position <- factor(plot_tab$Position, levels = c('First', 'Total Average', 'Last'))
sorters <- plot_tab %>% 
  select(Title, `Vocab Rate`, `Word Count`) %>% 
  unique()
uni <- unique(plot_tab$Title)
genres <-  c('All') %>% 
  append(unique(plot_tab$Genre))
authors <-  c('All') %>% 
 append(unique(plot_tab$Author))

# -!-! ADDING DASHBOARD ALL HANDS ON DECK !-!-


# Define UI ----
ui <- fluidPage(
  titlePanel("Sentence Lengths Across Literary Classics"),
  
  sidebarLayout(
    sidebarPanel(
      h2("Filter Options"),
      selectInput("selectG", h5("Filter by Genre"),
                  choices = genres, selected = 1),
      selectInput("selectA", h5("Filter by Author"),
                choices = authors, selected = 1),
      selectInput("selectS", h5("Sort by Special Metric"),
              choices = c('None', 'Vocab Rate', 'Word Count'), selected = 1)),

    mainPanel(
      plotOutput('shiny_plot')
    )
  )
)

# Define server logic ----
server <- function(input, output) {
  

  lvl <- reactive({if(input$selectS != "None") {
    sorters[order(sorters[input$selectS]),]$Title
  } else {
    uni
  }})


# Create grouped bar chart for each title, grouped by author
  output$shiny_plot <- renderPlot(
# ggp <- reactive(
    plot_tab %>% 
      filter(str_detect(Genre, ifelse(input$selectG == "All", "", input$selectG))) %>%  
      filter(str_detect(Author, ifelse(input$selectA == "All", "", input$selectA))) %>%
      ggplot(aes(fill=Author, alpha=Position, y=Length, x=factor(Title, level = lvl()))) +
      geom_bar(position="dodge", stat="identity") + 
      theme(axis.text.x=element_text(angle = -40, hjust = 0)) +
      
  # NOTE --SORTED
      # NOTE The facet grid will need to go in order to order the books by wordcount or vocab if I 
      # decide to add that functionality
  #    facet_grid(cols = vars(Author), scales="free") +
  #    facet_grid(cols = ifelse(input$selectS == "None", vars(Author), NULL), scales="free") +
  #    facet_grid(cols = switch(x(), vars(Author), NULL), scales="free") +
  # NOTE --SORTED
    
      scale_alpha_manual(values = c(0.3, 0.6, 1)) +
      scale_y_continuous(breaks = seq(0, 90, 10)) +
      scale_x_discrete(labels = label_wrap_gen(25)) +
      xlab('Book Title') +
      ylab('Words per Sentence')
  )
  
  #output$shiny_plot <- renderPlot(
  #  if(input$selectS == 'None') {
  #    ggp +
  #    facet_grid(cols = vars(Author), scales="free")
  #  } else{
  #   ggp
  #  }
  #)
  
}


# Run the app ----
shinyApp(ui = ui, server = server)

