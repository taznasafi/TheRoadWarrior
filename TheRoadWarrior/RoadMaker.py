import arcpy
import sys
import os
import logging
import time
import traceback
from TheRoadWarrior import get_path, _input_path
import pandas as pd



formatter = ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename=r"./logs/{}_Log_{}.csv".format(__name__.replace(".", "_"), time.strftime("%Y_%m_%d_%H_%M")),
                                 level=logging.DEBUG, format=formatter)

arcpy.env.parallelProcessingFactor = "80%"


class Road_maker:
    def __init__(self, input_path=None, inputGDB=None, inputGDB2 = None, referenceGDB = None,
                 outputGDBname=None, outputpathfolder=None, outputfolder_name = None, outputGDB=None):
        self.inputpath = input_path
        self.inputGDB = inputGDB
        self.inputGDB2 = inputGDB2
        self.referenceGDB = referenceGDB
        self.outputGDBName = outputGDBname
        self.outputpathfolder = outputpathfolder
        self.outputfolder_name = outputfolder_name
        self.outputGDB = outputGDB
        self.fcList = []
        self.input_dict = get_path.defaultdict(list)
        self.output_dict = get_path.defaultdict(list)
        self.wildcard_dict = dict()
        self.dry_run=False

    def create_folder(self):
        print("creating folder")
        logging.info("creating folder")
        try:
            if not os.path.exists(self.outputpathfolder):
                os.makedirs(self.outputpathfolder)

        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            message = "Traceback info:\n" + tbinfo
            print(message)
            logging.warning(message)

    def create_gdb(self):
        print("Creating gdb")
        logging.info("Creating GDB named: {}".format(self.outputGDBName))
        try:
            arcpy.CreateFileGDB_management(out_folder_path=self.outputpathfolder, out_name=self.outputGDBName)
            print(arcpy.GetMessages(0))
            logging.info("created GDB, messages: {}".format(arcpy.GetMessages(0)))


        except arcpy.ExecuteError:
            msgs = arcpy.GetMessages(2)
            arcpy.AddError(msgs)
            print(msgs)
            logging.info(msgs)
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)
            logging.info(pymsg)
            logging.info(msgs)

    def add_field(self, field_name=None, field_type=None):
        try:

            for fc in self.input_dict['step_01'][0]:
                print(fc)
                if self.dry_run is False:

                    arcpy.AddField_management(fc, field_name=field_name, field_type=field_type)
                    print(arcpy.GetMessages())
                    logging.info("added a field to {}".format(fc))
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)
            logging.info(pymsg)
            logging.info(msgs)

    def calculate_Field(self, field_name=None, code=None, code_block=None):

        try:

            for fc in self.input_dict['step_01'][0]:
                print(fc)
                if self.dry_run is False:

                    arcpy.CalculateField_management(fc,field_name, expression=code, expression_type="PYTHON3",
                                                    code_block=code_block)
                    print(arcpy.GetMessages())
                    logging.info("calculated a field to {}".format(fc))

        except:

            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
            print(pymsg)
            print(msgs)
            logging.info(pymsg)
            logging.info(msgs)


    def load_roads_into_pandas_table(self, field=None, export_group_df =False, groupby_field=None, output_csv_name=None,
                                     merge_group_challenge_grids=False):

        print("grouping table and exporting")

        if self.dry_run is False:

            print("adding all of the fc's into memory using these columns : {}\n".format(field))
            df = get_path.pathFinder.return_merged_tables_from_fc_list(self.inputGDB,field=field)

            df['drive_test_road'] = 0
            df.drive_test_road.loc[
                (df.MTFCC == 'S1100') | (df.MTFCC == 'S1200') | (df.MTFCC == 'S1400') | (df.MTFCC == 'S1500') | (
                            df.MTFCC == 'S1640') | (df.MTFCC == 'S1740')] = 1

            df_road_mile_pivot = pd.DataFrame(
                df.loc[df.drive_test_road == 1].pivot(index="id", columns='MTFCC', values='road_miles'))

            df_road_mile_pivot.reset_index(inplace=True)
            df_road_mile_pivot.fillna(0, inplace=True)


            df_road_mile_pivot['road_mile_per_grid_mfi'] = df_road_mile_pivot['S1100'] +\
                                                            df_road_mile_pivot['S1200'] +\
                                                            df_road_mile_pivot['S1400'] +\
                                                            df_road_mile_pivot['S1500'] +\
                                                            df_road_mile_pivot['S1640'] +\
                                                            df_road_mile_pivot['S1740']

            if export_group_df is True:

                print("Grouping and summing the table using the following fields: {}\n".format(groupby_field))
                df_grouped_sum = df.groupby(groupby_field)['road_miles'].sum()
                print('exporting table to ouput folder: {}\n'.format(os.path.join(self.outputpathfolder,
                                                                                  output_csv_name)))

                df_grouped_sum.to_csv(os.path.join(self.outputpathfolder, output_csv_name), header=True)

            if merge_group_challenge_grids is True:

                grid_cell_challenged_single_provider_csv = pd.read_csv(self.inputpath)
                print("joining tables\n")
                joined_df = pd.merge(left=grid_cell_challenged_single_provider_csv, left_on='grid_id',
                                     right=df_road_mile_pivot, right_on='id', how="outer")
                del df, df_road_mile_pivot

                print('exporting raw table to ./data/input just incase\n')
                joined_df.to_csv(os.path.join(_input_path,"raw_join_road_miles_and_challenged_grid_cells_out_join.csv" ), header=True)

                joined_df['MFI_roads'] = 1
                joined_df.loc[(joined_df.road_mile_per_grid_mfi.isna()), 'MFI_roads'] = 0

                joined_df_group = joined_df.groupby(
                    ['state_fips', 'challenge_flag', 'single_provider_ineligible_area_flag', 'MFI_roads']).agg(
                    {'area_sq_meters': 'sum',
                     'water_area_sq_meters': 'sum',
                     'non_water_area_sq_meters': 'sum',
                     'eligible_area_sq_meters': 'sum',
                     'ineligible_area_sq_meters': 'sum',
                     'single_provider_ineligible_area_sq_meters': 'sum',
                     'challenged_area_sq_meters': 'sum',
                     'tested_area_sq_meters': 'sum',
                     'non_tested_area_sq_meters': 'sum',
                     "road_mile_per_grid_mfi": 'sum'})

                challenged_roads = joined_df.loc[(joined_df.challenge_flag == 1)].groupby(by=groupby_field)[
                    'S1100', 'S1200', 'S1400','S1500','S1640','S1740','road_mile_per_grid_mfi'].sum()

                single_area_ineligible_roads = joined_df.loc[(joined_df.single_provider_ineligible_area_flag==1)].groupby(by=groupby_field)[
                    'S1100', 'S1200', 'S1400','S1500','S1640','S1740','road_mile_per_grid_mfi'].sum()

                challenge_single_area_roads = joined_df.loc[(joined_df.challenge_flag == 1)&(joined_df.single_provider_ineligible_area_flag == 1)].groupby(by=groupby_field)[
                    'S1100', 'S1200', 'S1400','S1500','S1640','S1740','road_mile_per_grid_mfi'].sum()

                for filename, df_roads in {'total_challenged_roads_by_state_by_grid.csv':challenged_roads,
                            'total_road_miles_in_single_provider_ineligible.csv':single_area_ineligible_roads,
                                           'challenged_and_signle_area_ineligible_road_miles.csv':challenge_single_area_roads,
                                           'groupby_state_challengeFlage_SingleAreaIneligible_MFIroads_Sums.csv':joined_df_group}.items():

                    print('exporting table to ouput folder: {}\n'.format(
                        os.path.join(self.outputpathfolder, filename)))
                    df_roads.to_csv(os.path.join(self.outputpathfolder,filename), header=True)
        else:
            print("dry running")

