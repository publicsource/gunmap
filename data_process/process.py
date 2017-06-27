from secret import *
import csv, re, agate

data_file = data_path + '20170620-LMPD-homicide-data.csv'

def agate_clean():
    new_homicides = data_path + '20170620-LMPD-homicide-data-CLEAN.csv'
    text_type = agate.Text()
    homicides = agate.Table.from_csv(data_file)

    def new_victim(row):
        victim = row['Victim']
        digits = re.search(r'\d+$', victim)
                
        if digits is not None:
            name_race_gender = re.sub(digits.group(), '', victim).lstrip().rstrip()
                            
            if name_race_gender.endswith('/'):
                name = name_race_gender[:-4]
            else:
                name = name_race_gender[:-3]
        else:
            name = row['Victim']
            
        return name
            
    def new_gender(row):
        victim = row['Victim']
        digits = re.search(r'\d+$', victim)
                
        if digits is not None:
            name_race_gender = re.sub(digits.group(), '', victim).lstrip().rstrip()
                            
            if name_race_gender.endswith('/'):
                gender = name_race_gender[-2]
            else:
                gender = name_race_gender[-1]
        else:
            gender = row['Sex']
        
        return gender
            
    def new_race(row):
        victim = row['Victim']
        digits = re.search(r'\d+$', victim)
                
        if digits is not None:
            name_race_gender = re.sub(digits.group(), '', victim).lstrip().rstrip()
                            
            if name_race_gender.endswith('/'):
                race = name_race_gender[-4]
            else:
                race = name_race_gender[-3]
        else:
            race = row['Race']
            
        return race
        
    def new_age(row):
        victim = row['Victim']
        digits = re.search(r'\d+$', victim)
                
        if digits is not None:
            age = digits.group()
        else:
            age = row['Age']
            
        return age
            
        
    new_table = homicides.compute([
        ('new_victim', agate.Formula(text_type, new_victim)),
        ('new_gender', agate.Formula(text_type, new_gender)),
        ('new_race', agate.Formula(text_type, new_race)),
        ('new_age', agate.Formula(text_type, new_age))
    ])
    
    #new_table.print_table()
    new_table.to_csv(new_homicides)



def clean_columns():
    with open(data_path) as csvfile:
        reader = csv.DictReader(csvfile)
                
        for row in reader:
            victim = row.get('Victim')
            digits = re.search(r'\d+$', victim)
            
            if digits is not None:
                age = digits.group()
                name_race_gender = re.sub(digits.group(), '', victim).lstrip().rstrip()
                                
                if name_race_gender.endswith('/'):
                    name = name_race_gender[:-4]
                    gender = name_race_gender[-2]
                    race = name_race_gender[-4]
                else:
                    name = name_race_gender[:-3]
                    gender = name_race_gender[-1]
                    race = name_race_gender[-3]
            
            
            
agate_clean()
#clean_columns()