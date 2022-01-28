from __future__ import absolute_import
import argparse
import logging
import re
import numpy as np
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


class Printer(beam.DoFn):
  def process(self,data_item):
    print(data_item)


class split_line_join_data_1(beam.DoFn):

  def process(self,element):

    user, gender, age, address, date_joined = element.split(sep=',')


    return [(user, {'gender': gender,
                    'age': age,
                    'address': address,
                    'date_joined': date_joined})]

class split_line_join_data_2(beam.DoFn):

  def process(self,element):

    order, user = element.split(sep=',')
    user = user.strip(' ')

    return [(user, order)]


class collect_gender_order(beam.DoFn):

  def process(self,element):

    return [(element[1]['input_join_data_1'][0]['gender'], len(element[1]['input_join_data_2']))]


class calc_gender_order(beam.DoFn):

  def process(self,element):

    if element[0] == 'Female':

      print('Average number of female orders = ', np.mean(element[1]))

    if element[0] == 'Male':

      print('Average number of male orders = ', np.mean(element[1]))

    return element

class collect_gender_order(beam.DoFn):

  def process(self,element):

    return [(element[1]['input_join_data_1'][0]['gender'], len(element[1]['input_join_data_2']))]

class collect_age_bracket(beam.DoFn):

  def process(self,element):

    if int(element[1]['input_join_data_1'][0]['age']) < 25: element = ('15-25',len(element[1]['input_join_data_2']))
    elif int(element[1]['input_join_data_1'][0]['age']) < 35: element = ('25-35', len(element[1]['input_join_data_2']))
    elif int(element[1]['input_join_data_1'][0]['age']) < 45: element = ('35-45', len(element[1]['input_join_data_2']))
    elif int(element[1]['input_join_data_1'][0]['age']) <= 55: element = ('45-55', len(element[1]['input_join_data_2']))

    return [element]

class calc_age_bracket_avg(beam.DoFn):

  def process(self,element):

    if element[0] == '15-25':

      print('Average number of 15-25 orders = ', np.mean(element[1]))

    if element[0] == '25-35':

      print('Average number of 25-35 orders = ', np.mean(element[1]))

    if element[0] == '35-45':

      print('Average number of 35-45 orders = ', np.mean(element[1]))

    if element[0] == '45-55':

      print('Average number of 45-55 orders = ', np.mean(element[1]))

    return element

def run(argv=None, save_main_session=True):
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--input',
      dest='input',
      required=True,
      help='Input file to process.')
  parser.add_argument(
      '--output',
      dest='output',
      required=True,
      help='Output file to write results to.')
  known_args, pipeline_args = parser.parse_known_args(argv)

  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

  # Create the initial PCollection
  p = beam.Pipeline(options=pipeline_options)

  input_join_data_1 = (
      p
      | 'read_join_data_1' >> ReadFromText(known_args.input, skip_header_lines=True)
      | 'split_line_join_data_1' >> beam.ParDo(split_line_join_data_1())
      )

  input_join_data_2 = (
      p
      | 'read_join_data_2' >> ReadFromText('C:\\Users\\MSI\\Desktop\\day_4_tut\\orders.csv', skip_header_lines=True)
      | 'split_line_join_data_2' >> beam.ParDo(split_line_join_data_2())
      )

  joined_data = (
      {'input_join_data_1': input_join_data_1, 'input_join_data_2': input_join_data_2}
      | beam.CoGroupByKey()
      )

  gender_order = (
      joined_data
      | 'collect_gender_order' >> beam.ParDo(collect_gender_order())
      | 'groupby gender_order' >> beam.GroupByKey()
      | 'calc_gender_order' >> beam.ParDo(calc_gender_order())
      # | 'Print the data' >> beam.ParDo(Printer())
      )
  age_bracket = (
      joined_data
      | 'collect_age_bracket' >> beam.ParDo(collect_age_bracket())
      | 'groupby age_bracket' >> beam.GroupByKey()
      | 'calc_age_bracket_avg' >> beam.ParDo(calc_age_bracket_avg())
      # | 'Print the data' >> beam.ParDo(Printer())
      )

  result = p.run()
  result.wait_until_finish()

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
