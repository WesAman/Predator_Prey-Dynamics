# Predator_Prey-Dynamics
Exploration of the application of the Lotka-Volterra Model on predator-prey population data using python

Overview:
Experimenting with Lotka-Volterra Model, it attempts to model the population dynamics of two species: a predator species and a prey species. 

The model assumes that:
•The population of each species is continuous (e.g. having 0.4 of an animal is possible) and time is continuous; which are necessary assumptions in any model based on differential equations.

•In the absence of predators, the prey species experiences unbounded growth.

•In the absence of prey, the predator species decays to zero.

•The decay rate of the prey species is proportional to the population size of the predator species.

•The growth rate of the predator species is proportional to the population size of the prey species.

For this project I wanted to explore the behavior of this simulation, addressing the following:


1)what The types of outcomes the simulation can have, and how common they appear to be?

2)The conditions under which it appears the Lotka-Volterra Model describes the simulation results well?

3)How the main three simulation parameters ("breed_time", "energy_gain", and "breed_energy") should relate to the four Lotka-Volterra parameters (a, b c, and d)?

4) The difference in results for the two types of setups the program implements?

Findings:

1) 
The Wa-Tor simulation can have different types of outcomes, depending on the values of its parameters. Some common outcomes include:
-Stable equilibrium: where the populations of sharks and fish reach a balance, with no major fluctuations over time.

-Oscillations: where the populations of sharks and fish fluctuate over time, but without any long-term trends.

-Extinction: where one or both populations become extinct due to lack of food (fish) or predators (sharks).

-Chaotic behavior: where the populations of sharks and fish exhibit complex, unpredictable behavior over time.

The frequency of these outcomes depends on the initial conditions and the values of the simulation parameters. For example, increasing the energy gain of the fish may lead to more stable outcomes, while decreasing it may lead to more extinctions.

2)
The Lotka-Volterra Model describes the simulation results well under certain conditions, such as:

-A large number of individuals in each population.

-No spatial structure or migration.

-No age structure or other demographic factors.

-No environmental variation or stochasticity.

When these conditions are met, the Lotka-Volterra Model can provide a useful approximation of the dynamics of the Wa-Tor simulation. However, I found that in more complex scenarios, tinkering and involving other models/simulation methods may be needed.

3)
The main three simulation parameters ("breed_time", "energy_gain", and "breed_energy") can be related to the four Lotka-Volterra parameters as follows:

-a (predation rate): influenced by the breed_time parameter, which determines how often sharks can breed and thus increase their predation rate.

-b (conversion efficiency): influenced by the energy_gain parameter, which determines how much energy the fish gain from each time step and thus how efficient they are at converting resources into population growth.

-c (intraspecific competition): not directly influenced by any of the parameters, but can emerge from the dynamics of the simulation as a result of limited resources and population density.

-d (death rate): influenced by the breed_energy parameter, which determines how much energy a fish must have to breed and thus avoid being eaten by sharks.

4) The two types of setups implemented in the Wa-Tor program are:

-A toroidal grid, where individuals at the edges wrap around to the opposite side. This can lead to more spatially structured dynamics and longer persistence of populations.

-A bounded grid, where individuals at the edges are lost. This can lead to more chaotic and unpredictable dynamics, especially when the populations are small.
The difference in results between these setups depends on the values of the parameters and the initial conditions. In general, the toroidal grid may be more suitable for studying spatially structured dynamics, while the bounded grid may be more suitable for studying extinction and recovery processes.
