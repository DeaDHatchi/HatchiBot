import random


class Player:
    def __init__(self, health, mana, health_potion_count, name):
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.name = name
        self.health_potion_count = health_potion_count

    def damage_done(self):
        return random.randint(1, 20)

    def damage_taken(self, cost):
        self.health -= abs(cost)

    def healing(self, cost):
        self.health += abs(cost)

    def mana_spent(self, cost):
        self.mana -= abs(cost)

    def mana_gained(self, cost):
        self.mana += abs(cost)

    def crit_miss_chance(self, spell, damage_done):
        crit = random.randint(1, 20)
        if crit == 20:
            damage_done = damage_done * 2
            print(f"{spell} critically hit!")
        elif crit == 1:
            damage_done = damage_done * 0
            print(f"{spell} misses!")
        else:
            damage_done = damage_done
        return damage_done

    def calc_damage(self, spell_name):
        return self.crit_miss_chance(spell_name, self.damage_done())

    def cast_efficient_spell(self, spell_name):
        self.mana_spent(10)
        return self.result_damage_done(spell_name, self.calc_damage(spell_name))

    def cast_powerful_spell(self, spell_name):
        self.mana_spent(25)
        return self.result_damage_done(spell_name, self.calc_damage(spell_name))

    def cast_evocation(self):
        damage_done = 0
        self.mana_gained(self.max_mana)
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        print(f"{self.name} casts Evocation")
        print(f"{self.name} has refilled their mana to {self.mana} mana!")
        return damage_done

    def use_healthpotion(self):
        self.healing(20)
        self.health_potion_count -= 1
        damage_done = 0
        print(f"{self.name} uses a Healthstone!")
        print(f"{self.name} gains 20 health")
        return damage_done

    def result_damage_done(self, spell_name, damage_done):
        print(f"{self.name} casts {spell_name}")
        print(f"{self.name} deals {damage_done} damage")
        return damage_done

    # all the options given for a turn
    def turn_action(self):
        action = input("Casting a Weak Spell, Strong Spell or Evocation, or using a Healthpotion?:  ").lower()
        damage_done = 0
        if action == "weak spell":
            if self.mana >= 10:
                damage_done = attacking_player.cast_efficient_spell(input("Name of Spell: "))
                enemy_player.damage_taken(damage_done)
            else:
                print(f"That spell costs 10 mana and you have {self.mana} mana!")
                self.turn_action()
        elif action == "strong spell":
            if self.mana >= 25:
                damage_done = attacking_player.cast_powerful_spell(input("Name of Spell: "))
                enemy_player.damage_taken(damage_done)
            else:
                print(f"That spell costs 25 mana and you have {self.mana} mana!")
                self.turn_action()
        elif action == "evocation":
            damage_done = attacking_player.cast_evocation()
        else:
            if self.health_potion_count > 0:
                damage_done = attacking_player.use_healthpotion()
            else:
                print("You don't have any health potions!")
                self.turn_action()
        if action == "evocation":
            self.mana = self.mana
        else:
            self.mana += 5
        return damage_done


# Initialize Values, and determine who attacks first.
player1 = Player(name="Hatchi", health=100, mana=100, health_potion_count=1)
player2 = Player(name="Galumian", health=100, mana=100, health_potion_count=1)

attacking_player = random.choice([player1, player2])

if attacking_player == player1:
    enemy_player = player2
else:
    enemy_player = player1

game_status = True
count = 1  # this keeps track of what round it is

while game_status:
    #Turn Action
    print(f"it is {attacking_player.name}'s Turn. They have {attacking_player.mana} mana remaining")
    damage = attacking_player.turn_action()

    #check for win condition
    if enemy_player.health <= 0:
        print(f"Congratulations {attacking_player.name} you win!")
        game_status = False
    else:
        count += .5                    #a round is when both sides do their move
        if attacking_player.mana == attacking_player.max_mana:
            pass
        else:
            print(f"{attacking_player.name} has regained 5 mana")
        print(f"{enemy_player.name} took {damage} damage and has {enemy_player.health} health remaining\n")
        attacking_player, enemy_player = enemy_player, attacking_player
