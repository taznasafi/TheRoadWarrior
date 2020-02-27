from bin import _01, _02
# 01 add field and calculate length
print("\n-------------------- 01 -----------------------\n")

print("\nadding_fields")



_01.add_field_and_calculate_length(dry_run=False,
                                   add_fields=True, state_wild_card='*_78_*')
print('\nCreating Grid ID')
_01.add_field_and_calculate_length(dry_run=False,
                                   create_id=True, state_wild_card='*_78_*')
print("\nCalculating RoadMiles")
_01.add_field_and_calculate_length(dry_run=False,
                                   calculate_Raod_miles=True,  state_wild_card='*_78_*')

print("\n-------------------- 02 -----------------------\n")

# 02 Join challenge grid cell to road miles, then copy features to a new gdb

# 02A create road miles by state by MTFCC and sum roadmiles
print("\n Grouping and Exporting CSV")
_02.export_road_miles_to_csv(dry_run=True,
                             export_group_df=True,csv_name='road_miles_by_state_by_mtfcc.csv')

_02.export_road_miles_to_csv(dry_run=True,merge_group_challenge_grids=True)
