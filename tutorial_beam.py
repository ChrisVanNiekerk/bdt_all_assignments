from __future__ import absolute_import
import argparse
import logging
import re
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


class Printer(beam.DoFn):
  def process(self,data_item):
    print(data_item)

class split_line(beam.DoFn):

  def process(self,element):

    user, gender, age, address, date_joined = element.split(sep=',')

    return [{'user': user, 'gender': gender, 'age': age, 'address': address, "date_joined": date_joined}]

class format_task1(beam.DoFn):

  def process(self, element):

    element['address'] = element['address'].strip(' ')
    element['address'] = element['address'].replace('-', ',')
    element['date_joined'] = element['date_joined'].replace('/', '-')

    return [";".join(element.values())]

class format_task2(beam.DoFn):

  def process(self, element):

    element['address'] = element['address'].strip(' ')
    element['address'] = element['address'].replace('-', ',')
    element['date_joined'] = element['date_joined'].replace('/', '-')

    return [element]

class CollectGender(beam.DoFn):
  def process(self, element):

    # Returns a list of tuples containing Gender and Open value
    return [(element['gender'],1)]

class CalcGender(beam.DoFn):

  def process(self,element):

    print('Number of ', element[0], ' = ', sum(element[1]))

    return element

class CollectDate(beam.DoFn):
  def process(self, element):
    # Returns a list of tuples containing Date and Open value
    return [(element['date_joined'],1)]

class CalcDate(beam.DoFn):

  def process(self,element):

    print('Number of customers joined on', element[0], ' = ', sum(element[1]))

    return element

class CollectState(beam.DoFn):
  def process(self, element):
    # Returns a list of tuples containing State and Open value

    return [(element['address'].split(sep=',')[1],1)]

class CalcState(beam.DoFn):

  def process(self,element):

    print('Number of customers in', element[0], ' = ', sum(element[1]))

    return element

class split_line_join_data_1(beam.DoFn):

  def process(self,element):

    # print('I am inside split line function')

    user, gender, age, address, date_joined = element.split(sep=',')


    return [(user, {'gender': gender,
                    'age': age,
                    'address': address,
                    'date_joined': date_joined})]


class split_line_join_data_2(beam.DoFn):

  def process(self,element):

    # print('I am inside split line function')

    order, user = element.split(sep=',')
    user = user.strip(' ')

    # print(order)

    return [(user, order)]


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

  # Read the input file into a PCollection & split
  input_data = (
      p
      | 'read' >> ReadFromText(known_args.input, skip_header_lines=True)
      | 'split_line' >> beam.ParDo(split_line())
      )

  task1 = (
      input_data
      | 'format' >> beam.ParDo(format_task1())
      | 'write' >> WriteToText(known_args.output, header = 'User;Gender;Age:Address;Date joined')
      )

  task2_gender_gap = (
      input_data
      | 'format_2' >> beam.ParDo(format_task2())
      | 'collect_gender' >> beam.ParDo(CollectGender())
      | 'GroupBy Gender' >> beam.GroupByKey()
      | 'gender_comp' >> beam.ParDo(CalcGender())
      )

  task2_creation_date = (
      input_data
      | 'format_3' >> beam.ParDo(format_task2())
      | 'collect_date' >> beam.ParDo(CollectDate())
      | 'GroupBy Date' >> beam.GroupByKey()
      | 'date_comp' >> beam.ParDo(CalcDate())
      )

  task2_state = (
      input_data
      | 'format_4' >> beam.ParDo(format_task2())
      | 'collect_state' >> beam.ParDo(CollectState())
      | 'GroupBy State' >> beam.GroupByKey()
      | 'state_comp' >> beam.ParDo(CalcState())
      )

  input_join_data_1 = (
      p
      | 'read_join_data_1' >> ReadFromText(known_args.input)
      | 'split_line_join_data_1' >> beam.ParDo(split_line_join_data_1())
      # | 'Print the data' >> beam.ParDo(Printer())
      )

  input_join_data_2 = (
      p
      | 'read_join_data_2' >> ReadFromText('C:\\Users\\MSI\\Desktop\\day_4_tut\\orders.csv')
      | 'split_line_join_data_2' >> beam.ParDo(split_line_join_data_2())
      # | 'Print the data' >> beam.ParDo(Printer())
      )

  joined_data = (
      {'input_join_data_1': input_join_data_1, 'input_join_data_2': input_join_data_2}
      | beam.CoGroupByKey()
      | 'Print the data' >> beam.ParDo(Printer())
      )

  result = p.run()
  result.wait_until_finish()

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
