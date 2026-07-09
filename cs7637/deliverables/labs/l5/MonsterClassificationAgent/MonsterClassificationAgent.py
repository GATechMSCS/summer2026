class MonsterClassificationAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.

        self.attributes = ["size", "color", "covering",
                           "foot-type", "leg-count", "arm-count",
                           "eye-count", "horn-count", "lays-eggs",
                           "has-wings", "has-gills", "has-tail"]

    def solve(self, samples, new_monster):
        #Add your code here!
        #
        #The first parameter to this method will be a labeled list of samples in the form of
        #a list of 2-tuples. The first item in each 2-tuple will be a dictionary representing
        #the parameters of a particular monster. The second item in each 2-tuple will be a
        #boolean indicating whether this is an example of this species or not.
        #
        #The second parameter will be a dictionary representing a newly observed monster.
        #
        #Your function should return True or False as a guess as to whether or not this new
        #monster is an instance of the same species as that represented by the list.

        pos_samps = [known_pos for known_pos, is_pos in samples if is_pos]
        neg_samps = [known_neg for known_neg, is_pos in samples if not is_pos]

        score = 0

        for attribute in self.attributes:

            new_mon_att = new_monster[attribute]

            pos_matches = sum(1 for monster in pos_samps if monster[attribute] == new_mon_att)
            neg_matches = sum(1 for monster in neg_samps if monster[attribute] == new_mon_att)

            if pos_matches > neg_matches:
                score += 1

            elif neg_matches > pos_matches:
                score -= 1

        return score > 0

