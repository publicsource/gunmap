from secret import *
import csv, re, agate, datetime

data_file = data_path + '20170620-LMPD-homicide-data.csv'
clean_homicides = data_path + '20170620-LMPD-homicide-data-GEOCODED.csv'

text_type = agate.Text()
date_type = agate.Date()
num_type = agate.Number()


#calculate year
def calc_year(row):
    return row['Date'].year
    
#calculate month
def calc_month(row):
    return row['Date'].month
    

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



def age_brackets():
    homicides = agate.Table.from_csv(clean_homicides)
        
    year_homicides = homicides.compute([
        ('year', agate.Formula(num_type, calc_year))
    ])
    
    years = []
    years_data = year_homicides.distinct('year').order_by('year')
    
    for year in years_data.rows:
        years.append(year['year'])
        
    for year in years:
        print year
        #year_homicides.where(lambda row: row['year'] == year).bins('new_age', start=0, end=100).print_bars('new_age', width=80)
        #year_homicides.where(lambda row: row['year'] == year).bins('new_age', count=10).print_bars('new_age', width=80)
        year_homicides.where(lambda row: row['year'] ==  year).bins('new_age', count=20, start=0, end=90).bar_chart('new_age', 'Count', img_path + str(year) +'_age_chart.svg')
        
        
def race_brackets():
    homicides = agate.Table.from_csv(clean_homicides)
        
    year_homicides = homicides.compute([
        ('year', agate.Formula(num_type, calc_year))
    ])
    
    years = []
    years_data = year_homicides.distinct('year').order_by('year')
    
    for year in years_data.rows:
        years.append(year['year'])
        
    for year in years:
        print year
        #year_homicides.where(lambda row: row['year'] == year).pivot('new_race').print_bars('new_race', width=80)
        year_homicides.where(lambda row: row['year'] ==  year).pivot('new_race').bar_chart('new_race', 'Count', img_path + str(year) +'_race_chart.svg')
        
        
def month_brackets():
    homicides = agate.Table.from_csv(clean_homicides)
        
    year_homicides = homicides.compute([
        ('year', agate.Formula(num_type, calc_year)),
        ('month', agate.Formula(num_type, calc_month))
    ])
    
    year_homicides.pivot('month').print_bars('month', width=80)
    
    #years = []
    #years_data = year_homicides.distinct('year').order_by('year')
    #
    #for year in years_data.rows:
    #    years.append(year['year'])
    #            
    #for year in years:
    #    print year
    #    year_homicides.where(lambda row: row['year'] == year).pivot('month').print_bars('month', width=80)



def clean_causes():
    new_homicides = data_path + '20170627-LMPD-homicides-clean-geo.csv'
    new_homicides_json = data_path + '20170627-LMPD-homicides-clean-geo.json'
    
    asphixia = ['Ashphyxiation', 'Asphyxia', 'Asphyxia ', 'axphyxia', 'Suffocation']
    stabbing = ['Stabbed', 'Stabbing', 'stabbing ']
    unknown = ['0', 'Undetermined', 'UNK']
    
    include_columns = [
        'date', 
        'year',
        'month',
        'report', 
        'location', 
        'new_victim', 
        'new_gender', 
        'new_race', 
        'new_age', 
        'new_cause',
        'bing_type',
        'bing_confidence',
        'bing_latitude',
        'bing_longitude']
    
    def rename(row):
        cause = row['Cause']
        if cause in asphixia:
            return 'Asphixia'
        elif cause in stabbing:
            return 'Stabbing'
        elif cause in unknown:
            return 'Unknown'
        elif cause == 'BFT':
            return 'Blunt force trauma'
        elif cause == 'GSW':
            return 'Gun shot wound'
        else:
            return cause.capitalize()
            
    homicides = agate.Table.from_csv(clean_homicides)
    
    clean_cause = homicides.compute([
        ('year', agate.Formula(num_type, calc_year)),
        ('month', agate.Formula(num_type, calc_month)),
        ('new_cause', agate.Formula(text_type, rename))
    ])
            
    refined_homicides = clean_cause.rename(slug_columns=True).select(include_columns)
    
    
    refined_homicides.to_csv(new_homicides)
    refined_homicides.to_json(new_homicides_json)
    
    #clean_cause.pivot('new_cause').print_bars('new_cause', 'Count', width=80)
            
    
clean_causes()
#month_brackets()
#race_brackets()
#age_brackets()           
#agate_clean()
