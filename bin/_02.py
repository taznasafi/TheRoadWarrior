from TheRoadWarrior import RoadMaker, get_path, _input_path, _output_path



def export_road_miles_to_csv(dry_run = True, export_group_df =False, merge_group_challenge_grids=False, csv_name=None):

    _02 = RoadMaker.Road_maker(
        inputGDB=get_path.path_links.road_by_state_by_grid_gdb,
        input_path=get_path.path_links.grid_cells_challenged_single_provider_ineligible_csv,
        outputpathfolder=_output_path)

    _02.dry_run = dry_run

    if export_group_df is True:
        _02.load_roads_into_pandas_table(export_group_df=True,field=['id','STATE_FIPS', 'MTFCC', 'road_miles'],
                                         groupby_field=['STATE_FIPS', "MTFCC"],
                                         output_csv_name=csv_name)
    if merge_group_challenge_grids is True:
        _02.load_roads_into_pandas_table(merge_group_challenge_grids=True,field=['id','STATE_FIPS', 'MTFCC', 'road_miles'],
                                         groupby_field=['state_fips'])

