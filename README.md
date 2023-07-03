# mccvshiny

Interactive App for exploring Monte Carlo Cross Validation predictions from the {mccv} package using Shiny for Python

## Objective

1. Showcase the MCCV algorithm. More details on the algorithm and use cases at [nickg.mccv.bio](nickg.mccv.bio)

2. Provide an online tool for 

   A. Setting and generating univariate prior distributions based on the t, beta, and normally distributed data.

   B. Generating MCCV prediction results based on specified univariate data distributions.

   C. Visualizing MCCV prediction results.

3. Opportunity for Nick to learn Shiny for Python

## Components

1. Data: N [0,1000] sample size parameter
   A. Normal data: mu [-5,5] and sigma [0,5] parameters
   B. Beta data: a [0,5] and b [0,5] parameters
   C. T data: mu [-5,5] and df [1,N-1] parameters


2. MCCV Parameterization

3. MCCV Tables

4. MCCV Plots


## Design


## Notes

- Following https://shiny.posit.co/py/docs/comp-r-shiny.html and https://shiny.posit.co/py/docs/install.html closely to get started