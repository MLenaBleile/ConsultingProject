def colname_mask(ACS_cols):
    race_dict = {'Black or African American alone':'B',
                    'White alone':'W',
                    'American Indian and Alaska Native alone':'I',
                    'Asian alone':'A',
                    'Native Hawaiian and Other Pacific Islander alone':'P',
                    'Some other race alone':'O',
                    'Two or more races':'T',
                    'White alone, not Hispanic or Latino':'w',
                    'Hispanic or Latino (of any race)':'H'}
    gender_dict = {'Male':'M',
                      'Female':'F'}
    age_dict = {'Population 5 to 17 years':'5-17',
                   'Population 18 to 34 years':'18-34',
                   'Population 18 to 64 years':'18-64',
                   'Population 35 to 64 years':'35-64',
                   'Population 65 to 74 years':'65-74',
                   'Population 65 years and over':'65+',
                   'Population 75 years and over':'75+',
                   'Population under 18 years':'0-18',
                   'Population under 5 years':'0-5',
                   '5 to 17 years':'5-17',
                   '18 to 34 years':'18-34',
                   '18 to 64 years':'18-64',
                   '35 to 64 years':'35-64',
                   '65 to 74 years':'65-74',
                   '75 years and over':'75+',
                   '65 years and over':'65+',
                   'Under 5 years':'0-5',
                   'Under 18 years':'0-18'}
    dis_dict = {'With an independent living difficulty':'ind',
               'With a hearing difficulty':'aud',
               'With an ambulatory difficulty':'amb',
               'With a cognitive difficulty':'cog',
               'With a vision difficulty':'vis',
               'With a self-care difficulty':'self'}
    perc_dict = {'Percent with a disability':'%'}
    blank_dict = {'AGE':'',
                 'DISABILITY TYPE BY DETAILED AGE':'',
                 'SEX':'',
                 'RACE AND HISPANIC OR LATINO ORIGIN':'',
                 'Estimate':'',
                  'Total civilian noninstitutionalized population':'',
                 }
    group_dict = {'Total':'tot',
                 'With a disability':'dis'}
    
    mask_dict = {**race_dict, **gender_dict,
                **age_dict, **dis_dict, 
                **perc_dict, **blank_dict,
                **group_dict}
    
    new_cols = []
    for i in ACS_cols:
        var_split = i.split('!!')
        new_name = '_'.join([mask_dict[j] for j in var_split if mask_dict[j]!=''])
        new_cols.append(new_name)
    rename_dict = dict(zip(ACS_cols, new_cols))
    return rename_dict
