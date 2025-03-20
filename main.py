from datetime import date
import random
import pickle
import time

TEST_OFFSET = 3
DATE = date.today()
DATE_STRING = DATE.strftime("%Y-%m-%d-%A")
DATE_int = int(DATE.strftime("%Y%m%d"))
DATE_int += TEST_OFFSET

class dummy_object():
    def __init__(self):
        self.day_of_week = 7

class Mulkuth_daily():
    def __init__(self, mulkuth_weekly):
        self.mulkuth_weekly = mulkuth_weekly
        self.mulkuth_weekly.settled = False
        self.date = DATE_STRING
        self.year, self.month, self.day, self.day_of_week = self.date.split('-')
        #turn the day of the week to an integer
        self.day_of_week = self.day_of_week.lower()
        self.day_of_week = self.day_of_week.replace('monday', '1')
        self.day_of_week = self.day_of_week.replace('tuesday', '2')
        self.day_of_week = self.day_of_week.replace('wednesday', '3')
        self.day_of_week = self.day_of_week.replace('thursday', '4')
        self.day_of_week = self.day_of_week.replace('friday', '5')
        self.day_of_week = self.day_of_week.replace('saturday', '6')
        self.day_of_week = self.day_of_week.replace('sunday', '7')
        self.day_of_week = int(self.day_of_week)
        self.day_of_week = (TEST_OFFSET + self.day_of_week) % 7
        if self.day_of_week == 0:
            self.day_of_week = 7

        if self.day_of_week == 1:
            self.class_count = 10
        elif self.day_of_week == 2:
            self.class_count = 4
        elif self.day_of_week == 3:
            self.class_count = 3
        elif self.day_of_week == 4:
            self.class_count = 8
        elif self.day_of_week == 5:
            self.class_count = 2
        else:
            self.class_count = -1

        self.PE_box_que = [] #PE-box will be stored as a list like [["class,1"], ["class,1"],["homework,3"]]
        self.total_energy = 0
        self.PE_box_que_dream = [] #for dream mode
        self.total_energy_dream = 0
        
        print(self.year, self.month, self.day, self.day_of_week)
        print(DATE_int)

    def ZAYIN(self,type):
        if type == "class":
            self.PE_box_que.append(["class",1])
            self.total_energy += 1
            self.class_count -= 1
        elif type == "pomodoro":
            self.PE_box_que.append(["pomodoro",1])
            self.total_energy += 1
        elif type == "pixel_art":
            self.PE_box_que_dream.append(["pixel_art",1])
            self.total_energy_dream += 1
        elif type == "coding":
            self.PE_box_que_dream.append(["coding",1])
            self.total_energy_dream += 1
    
    def TETH(self, type):
        if type == "unneed_homework":
            self.total_energy += 3
            self.PE_box_que.append(["unneed_homework",3])
        elif type == "unity":
            self.total_energy_dream += 3
            self.PE_box_que_dream.append(["unity",3])
        elif type == "new_game_idea":
            self.total_energy_dream += 3
            self.PE_box_que_dream.append(["new_game_idea",3])
    def HE(self, type):
        if type == "homework":
            self.total_energy += 5
            self.PE_box_que.append(["homework",5])
        elif type == "good_grade":
            self.total_energy += 5
            self.PE_box_que.append(["good_grade",5])
        elif type == "daily_full_attendance":
            self.total_energy += 5
            self.PE_box_que.append(["daily_full_attendance",5])
        elif type == "polish_idea":
            self.total_energy_dream += 5
            self.PE_box_que_dream.append(["polish_idea",5])
        elif type == "Aeprite":
            self.total_energy_dream += 5
            self.PE_box_que_dream.append(["Aeprite",5])
        if "落櫻" in self.mulkuth_weekly.qliphoth.EGO:
            self.total_energy += 2
            print("落櫻 bonus!!! PE-box +2")

    def WAW(self, type):
        if type == "midterm_good_grade":
            self.total_energy += 10
            self.PE_box_que.append(["midterm_good_grade",10])
        elif type == "final_good_grade":
            self.total_energy += 10
            self.PE_box_que.append(["final_good_grade",10])
        elif type == "weekly_full_attendance":
            self.total_energy += 10
            self.PE_box_que.append(["weekly_full_attendance",10])
        elif type == "fully_catch_up":
            self.total_energy_dream += 10
            self.PE_box_que_dream.append(["fully_catch_up",10])
        elif type == "game_jam_start":
            self.total_energy_dream += 10
            self.PE_box_que_dream.append(["game_jam_start",10])
        elif type == "game_jam_end":
            self.total_energy_dream += 10
            self.PE_box_que_dream.append(["game_jam_end",10])
        elif type == "start_project":
            self.total_energy_dream += 10
            self.PE_box_que_dream.append(["start_project",10])

    def ALEPH(self, type):
        pass


    def settlement(self):
        #this function will be called at the end of the day
        #it will store the final result into Mulkuth_weekly object
        #if the class count is 0, do HE("daily_full_attendance")
        #print the result
        print("=====================================")
        print("Today's result")
        print("PE-box que: ", self.PE_box_que)
        print("Total energy: ", self.total_energy)
        print("PE-box que dream: ", self.PE_box_que_dream)
        print("Total energy dream: ", self.total_energy_dream)
        print("=====================================")
        self.mulkuth_weekly.store(self)
        self.mulkuth_weekly.settlement(self)

    def store_without_settlement(self):
        print("=====================================")
        print("Today's result")
        print("PE-box que: ", self.PE_box_que)
        print("Total energy: ", self.total_energy)
        print("PE-box que dream: ", self.PE_box_que_dream)
        print("Total energy dream: ", self.total_energy_dream)
        print("=====================================")
        self.mulkuth_weekly.store(self)
        
        

    def print(self):
        print(self.PE_box_que)
        print(self.total_energy)
        print(self.PE_box_que_dream)
        print(self.total_energy_dream)



class Mulkuth_weekly():
    #this store every Mulkuth_daily object in a week
    #if a week is completed, it will be stored in a file
    def __init__(self, qliphoth):
        self.qliphoth = qliphoth
        self.week = []
        self.full_attendance = False
        self.weekly_energy = 0
        self.weekly_energy_dream = 0
        self.daily_class_attendance = 5
        self.day_of_week = 0

        self.settled = False #this is used to check if the previous day is settled
        #become False once a new day started, become true once the day is settled
        #if the previous day is not settled, automatically settle the previous day before starting a new day

    def store(self, mulkuth_daily):
        if self.day_of_week == mulkuth_daily.day_of_week:
            #replacing the old one
            self.week[-1] = mulkuth_daily
        else:
            self.week.append(mulkuth_daily)
            self.day_of_week = mulkuth_daily.day_of_week

        self.qliphoth.cache = self
        
    def settlement(self, mulkuth_daily):
        self.settled = True
        self.weekly_energy += mulkuth_daily.total_energy
        self.weekly_energy_dream += mulkuth_daily.total_energy_dream
        if mulkuth_daily.class_count == 0:
            self.daily_class_attendance -= 1
            print("Daily full attendance!!!")
            self.weekly_energy += 5


        if self.daily_class_attendance == 0:
            self.full_attendance = True
            self.weekly_energy += 10
            mulkuth_daily.total_energy += 10
            print("Weekly full attendance!!!")

        if "振翅" in self.qliphoth.EGO and mulkuth_daily.total_energy >= 15:
            self.weekly_energy += 2
            print("振翅 bonus!!! PE-box +2")

        print("This week's result")
        print("Weekly energy: ", self.weekly_energy)
        print("Weekly energy dream: ", self.weekly_energy_dream)
        print("Burn out: ", self.qliphoth.burn_out)
        print("Independent PE-box: ", self.qliphoth.independent_PE_box)
        print("=====================================")

        if self.weekly_energy >= 1 and self.weekly_energy_dream >= 1:
            self.pe_transform()

        if mulkuth_daily.day_of_week == 7:
            #print the result
            self.qliphoth.judgement(self)
            self.qliphoth.cache = self
        else:
            self.qliphoth.cache = self

        self.qliphoth.date = DATE_int

    def pe_transform(self):
        #allow daily gamble(X to turn 1 of each energy in to independent PE-box
        print("PE transform")
        trans = input("Do you want to transform 1 of each energy to independent PE-box? (y/n)")
        if trans == "y":
            self.weekly_energy -= 1
            self.weekly_energy_dream -= 1
            #2% chance of success
            for i in range(2):

                time.sleep(3)
                success = random.randint(1,100)
                if success <= 2:
                    #sleep for 3 seconds  

                    self.qliphoth.independent_PE_box += 1
                    
                    print("Transform success!!!")
                else:
                    print("Transform failed!!!")
            time.sleep(2)
        else:
            print("\n")
        

class Qliphoth():
    #this keeps track of E.G.O. , the burn out, and the indepedent PE-box
    def __init__(self):
        self.EGO = []
        self.burn_out = 0
        self.independent_PE_box = 0
        self.progress = [dummy_object()]
        self.cache = dummy_object() #this is used to store the latest Mulkuth_weekly object without judgement
        self.date = DATE_int

        self.ZAYIN = ["振翅","懺悔"]
        self.TETH = ["赤瞳","落櫻","決死之心"]
        self.HE = ["雷蔕希雅","小小銀河","魔彈","血之渴望","凝視"]
        self.WAW = ["以愛與恨之名","月光","穿刺極樂","提燈","大黃蜂","偽裝","湛藍之痕","赤紅之痕"]
        self.ALEPH = ["失樂園"]
        

    def judgement(self, mulkuth_weekly):
        self.progress.append(mulkuth_weekly)
        week_energy = mulkuth_weekly.weekly_energy
        week_energy_dream = mulkuth_weekly.weekly_energy_dream
        week_energy -= 75
        week_energy_dream -= 25
        if week_energy < 0:
            self.burn_out += 1
        if week_energy_dream < 0:
            self.burn_out += 1
        while week_energy >= 10:
            if self.burn_out > 0:
                self.burn_out -= 1
                week_energy -= 10
            else:
                self.independent_PE_box += 1
                week_energy -= 10
                print("you crafted 1 independent PE-box from energy")

        while week_energy_dream >= 25:
            if self.burn_out > 0:
                self.burn_out -= 1
                week_energy_dream -= 25
            else:
                self.independent_PE_box += 1
                week_energy_dream -= 25
                print("you crafted 1 independent PE-box from dream energy")

        print("Judgement")
        print("Full attendance: ", mulkuth_weekly.full_attendance)
        print("Burn out: ", self.burn_out)
        print("Independent PE-box: ", self.independent_PE_box)
        print("=====================================")
        if self.burn_out == 5:
            print("You failed your promise.")

        if self.burn_out >= 1:
            print("Burn out should be resolved before crafting EGO")
        elif self.independent_PE_box >= 10:
            print("You have enough independent PE-box to craft EGO")
            craft = input("Do you want to craft EGO? (y/n)")
            if craft == "y":
                self.EGO_crafting()
            else:
                print("\n")
        else:
            print("You need more independent PE-box to craft EGO")
        print("=====================================")

        #save a copy of this week
        self.save_copy()
        
    def save(self):
        with open('Qliphoth.pickle', 'wb') as f:
            pickle.dump(self, f)

    def save_copy(self):
        #save every week judgement in case of file corruption or new update
        with open('Qliphoth_copy.pickle', 'wb') as f:
            pickle.dump(self, f)

    def load(self,dummy):
        self.EGO = dummy.EGO
        self.burn_out = dummy.burn_out
        self.independent_PE_box = dummy.independent_PE_box
        self.progress = dummy.progress
        self.date = dummy.date
        self.cache = dummy.cache


    def EGO_crafting(self):
        print("***EGO crafting***")
        time.sleep(3)
        self.independent_PE_box -= 10
        EGO = random.randint(1,100)
        if EGO <= 50 and len(self.ZAYIN) > 0:
            self.EGO.append(self.ZAYIN.pop(random.randint(0,len(self.ZAYIN)-1)))
        elif EGO <= 80 and len(self.TETH) > 0:
            self.EGO.append(self.TETH.pop(random.randint(0,len(self.TETH)-1)))
        elif EGO <= 90 and len(self.HE) > 0:
            self.EGO.append(self.HE.pop(random.randint(0,len(self.HE)-1)))
        elif EGO <= 95 and len(self.WAW) > 0:
            self.EGO.append(self.WAW.pop(random.randint(0,len(self.WAW)-1)))
        elif EGO <= 99 and len(self.ALEPH) > 0:
            self.independent_PE_box += 11
            print("you crafted 11 independent PE-box")
            return
        else:
            self.EGO.append(self.ALEPH.pop(random.randint(0,len(self.ALEPH)-1)))

        print("EGO crafting result: ", self.EGO[-1])
        time.sleep(2)
        return

def run():
    qliphoth = Qliphoth()
    start_day = False
    day_index = DATE_int
    #look for the Qliphoth file
    try:
        with open('Qliphoth.pickle', 'rb') as f:
            dummy = pickle.load(f)
        qliphoth.load(dummy)
        print("Qliphoth file loaded")
    except:
        start_day = True
        print("Qliphoth file not found,start the First day")



    #check if the date is the same
    print ("Last settled date: ", qliphoth.date)
    print ("Today's date: ", day_index)
    if qliphoth.date == day_index and start_day == False:
        Weekly = qliphoth.cache
        Daily = qliphoth.cache.week[-1]
        print("Today's progress loaded")
        
    elif start_day == False:
        #check if the previous day is settled, if not, settle it
        if qliphoth.cache.settled == False:
            print("Previous day is not settled, automatically settle the previous day")
            print("=====================================")
            qliphoth.cache.settlement(qliphoth.cache.week[-1])
            qliphoth.save()
        if qliphoth.cache.day_of_week == 7:
            Weekly = Mulkuth_weekly(qliphoth)
            Daily = Mulkuth_daily(Weekly)
            print("New week and day created")
        else:
            Weekly = qliphoth.cache
            Daily = Mulkuth_daily(Weekly)
            print("New day created")
    else:
        Weekly = Mulkuth_weekly(qliphoth)
        Daily = Mulkuth_daily(Weekly)
        print("First day created")

    #this is the main loop
    while True:
        print("What do you want to do?")
        print("1. Attend a class")
        
        choice = input()
        if choice == "1":
            Daily.ZAYIN("class")
        elif choice == "2":
            Daily.ZAYIN("pomodoro")
        elif choice == "3":
            Daily.ZAYIN("pixel_art")
        elif choice == "4":
            Daily.ZAYIN("coding")
        elif choice == "5":
            Daily.TETH("unneed_homework")
        elif choice == "6":
            Daily.TETH("unity")
        elif choice == "7":
            Daily.TETH("new_game_idea")
        elif choice == "8":
            Daily.HE("homework")
        elif choice == "9":
            Daily.HE("good_grade")
        elif choice == "10":
            Daily.HE("daily_full_attendance")
        elif choice == "11":
            Daily.HE("polish_idea")
        elif choice == "12":
            Daily.HE("Aeprite")
        elif choice == "13":
            Daily.WAW("midterm_good_grade")
        elif choice == "14":
            Daily.WAW("final_good_grade")
        elif choice == "15":
            Daily.WAW("weekly_full_attendance")
        elif choice == "16":
            Daily.WAW("fully_catch_up")
        elif choice == "17":
            Daily.WAW("game_jam_start")
        elif choice == "18":
            Daily.WAW("game_jam_end")
        elif choice == "19":
            Daily.WAW("start_project")
        elif choice == "20":
            Daily.settlement()
            Daily.mulkuth_weekly.qliphoth.save()
            break
        elif choice == "21":
            Daily.store_without_settlement()
            Daily.mulkuth_weekly.qliphoth.save()
            print(qliphoth.date)
            break
        else:
            print("Invalid choice")
            continue

if __name__ == '__main__':
    
    '''TEST_OFFSET = -1
    while True: #test loop
        run()
        TEST_OFFSET += 1
        DATE = date.today()
        DATE_STRING = DATE.strftime("%Y-%m-%d-%A")
        DATE_int = int(DATE.strftime("%Y%m%d"))
        DATE_int += TEST_OFFSET
    '''
    run()