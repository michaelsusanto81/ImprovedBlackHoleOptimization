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
		R = random.random()
		for i in range(len(self.location)):			
			self.location[i] = self.location[i] + R * (best_star.location[i] - self.location[i])

	def is_absorbed(self, R, best_star):
		distance = 0
		for i in range(len(best_star.location)):
			distance += (best_star.location[i] - self.location[i])**2
		distance = math.sqrt(distance)

		return True if distance < R else False


class BlackHole:
	
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

	def generate_random_star(self):
		location = []
		for j in range(len(self.min_values_location)):				
			R = random.random()
			location.append(self.min_values_location[j] + R * (self.max_values_location[j] - self.min_values_location[j]))
		new_star = Star(location)
		return new_star

	def absorb_and_update(self, R, best_star):
		for star in self.stars:

			# if the star is in event horizon's radius
			if star.is_absorbed(R, best_star):
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

			# Inner Loop 2
			best_star = self.absorb_and_update(R, best_star)
		return best_star

# example uses 2 features (location) [Two Dimensional-Space example]
# the space's dimension is defined by the length of min_values_loc and max_values_loc array
num_stars = 100
min_values_loc = [0,0]
max_values_loc = [10,10]
max_iter = 1000
ibh = BlackHole(num_stars, min_values_loc, max_values_loc, max_iter)
best_star = ibh.run()

# Result
print("Maximum Optimization")
print("Max Location: %s" % (max_values_loc))
print("Best Star Location: %s" % (best_star.location))
print("Best Star Fitness Value: %.2f" % (best_star.get_fitval()))

# Error
error = [(max_values_loc[i] - best_star.location[i]) for i in range(len(best_star.location))]
print("Error Distance per Feature: %s" % (error))