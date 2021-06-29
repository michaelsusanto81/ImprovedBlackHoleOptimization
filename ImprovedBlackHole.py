"""
Authors:
- Evando Wihalim (1806205445)
- Michael Susanto (1806205653)

Implementation of
Improved Black Hole (Maximum) Optimization Algorithm by Deeb et al. (2020)
"""

import math, random

class Star:
	
	def __init__(self, location):
		self.location = location
		self.fitval = 0

	def get_fitval(self):
		fitval_sum = 0
		for i in range(len(self.location)):
			fitval_sum += self.location[i]
		self.fitval = fitval_sum
		return self.fitval

	def update_location(self, best_star):
		for i in range(len(self.location)):
      # improvement: use different random value for each attribute (random vector)
			R = random.random()
			self.location[i] = self.location[i] + R * (best_star.location[i] - self.location[i])

	def is_absorbed(self, R, best_star):
		distance = 0
		for i in range(len(best_star.location)):
			distance += (best_star.location[i] - self.location[i])**2
		distance = math.sqrt(distance)

		return True if distance < R else False


class ImprovedBlackHole:
	
	def __init__(self, num_stars, min_values_location, max_values_location, max_iter):
		self.num_stars = num_stars
		self.min_values_location = min_values_location
		self.max_values_location = max_values_location
		self.max_iter = max_iter

	def generate_initial(self):
		self.stars = []
		for i in range(self.num_stars):
			location = []
			for j in range(len(self.min_values_location)):				
				R = random.random()
				location.append(self.min_values_location[j] + R * (self.max_values_location[j] - self.min_values_location[j]))
			self.stars.append(Star(location))

	def get_best_star(self):
		best_star = self.stars[0]
		for i in range(1,len(self.stars)):
			if self.stars[i].get_fitval() > best_star.get_fitval():
				best_star = self.stars[i]
		return best_star

	def move_each_star(self, best_star):
		for star in self.stars:
			star.update_location(best_star)

			if star.get_fitval() > best_star.get_fitval():
				best_star = star
		return best_star	

	def calculate_radius_event_horizon(self, best_star):
		all_stars_fitval = 0
		for i in range(len(self.stars)):
			all_stars_fitval += self.stars[i].get_fitval()
		R = best_star.get_fitval() / all_stars_fitval
		return R

	def get_evolution_rate(self, iter):
		if (round(iter/self.max_iter,1)*10) % 2 == 0:
			return 0.75
		return 0.25

	def crossover(self):
		# get two random stars
		mid = (len(self.stars)-1) // 2
		a = random.randint(0, mid)
		b = random.randint(mid+1, len(self.stars)-1)

		star1 = self.stars[a]
		star2 = self.stars[b]

		# split points
		s1 = random.randint(0, len(self.min_values_location)-1)
		s2 = random.randint(0, len(self.min_values_location)-1)

		if s1 > s2:
			s1, s2 = s2, s1

		# do crossover
		for i in range(s1, s2+1):
			star1.location[i], star2.location[i] = star2.location[i], star1.location[i]

		# return star with higher fitness value
		return star1 if star1.get_fitval() > star2.get_fitval() else star2

	def generate_random_star(self):
		location = []
		for j in range(len(self.min_values_location)):				
			R = random.random()
			location.append(self.min_values_location[j] + R * (self.max_values_location[j] - self.min_values_location[j]))
		new_star = Star(location)
		return new_star

	def absorb_and_update(self, R, E, best_star):
		for star in self.stars:

			# if the star is in event horizon's radius
			if star.is_absorbed(R, best_star):
				new_star = None

        # improvement: there's a chance to crossover
				if random.random() <= E:
					# crossover
					new_star = self.crossover()
				else:
					# generate new random star
					new_star = self.generate_random_star()

				star.location = new_star.location
				star.fitval = new_star.fitval

			if star.get_fitval() > best_star.get_fitval():
				best_star = star
		return best_star

	def run(self):
		self.generate_initial()
		best_star = self.get_best_star()
		for i in range(self.max_iter):

			# Inner Loop 1
			best_star = self.move_each_star(best_star)

			R = self.calculate_radius_event_horizon(best_star)
			evolution_rate = self.get_evolution_rate(i+1)

			# Inner Loop 2
			best_star = self.absorb_and_update(R, evolution_rate, best_star)
		return best_star

# example uses 2 features (location) [Two Dimensional-Space example]
# the space's dimension is defined by the length of min_values_loc and max_values_loc array
num_stars = 100
min_values_loc = [0,0]
max_values_loc = [10,10]
max_iter = 1000
ibh = ImprovedBlackHole(num_stars, min_values_loc, max_values_loc, max_iter)
best_star = ibh.run()

# Result
print("Maximum Optimization")
print("Max Location: %s" % (max_values_loc))
print("Best Star Location: %s" % (best_star.location))
print("Best Star Fitness Value: %.2f" % (best_star.get_fitval()))

# Error
error = [(max_values_loc[i] - best_star.location[i]) for i in range(len(best_star.location))]
print("Error Distance per Feature: %s" % (error))