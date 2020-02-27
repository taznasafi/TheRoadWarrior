from TheRoadWarrior import RoadMaker, get_path


def add_field_and_calculate_length(dry_run=True, add_fields = False, create_id=False,
                                   calculate_Raod_miles = False, state_wild_card=None):
    if dry_run is False:



        _01 = RoadMaker.Road_maker(
            inputGDB=get_path.path_links.road_by_state_by_grid_gdb)

        if state_wild_card is None:
            _01.input_dict['step_01'].append(get_path.pathFinder(_01.inputGDB).get_path_for_all_feature_from_gdb(type='Polyline'))
        elif state_wild_card is not None:
            _01.input_dict['step_01'].append(
                get_path.pathFinder(_01.inputGDB).get_file_path_with_wildcard_from_gdb(wildcard=state_wild_card, data_type='All'))

        #make grid id = con(state_fips, gird_col, grid_row)
        if add_fields is True:
            _01.add_field(field_name='id',field_type='TEXT')
            _01.add_field('road_miles', 'DOUBLE')
        if create_id is True:
            _01.calculate_Field('id',
                                code="return_id('!STATE_FIPS!','!grid_col!', '!grid_row!')",
                                code_block='''def return_id(state_fips, grid_col, grid_row):
                                    return 'G'+str(state_fips).zfill(2)+str(grid_col).zfill(4)+str(grid_row).zfill(4)                                   
                               ''')
        if calculate_Raod_miles is True:
            _01.calculate_Field('road_miles', code="!SHAPE.geodesicLENGTH@MILES!")
