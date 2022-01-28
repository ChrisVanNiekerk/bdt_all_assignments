from __future__ import absolute_import
import argparse
import logging
import re
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

user_list = []
gender_list = []
age_list = []
address_list = []
date_joined_list = []
# i = 0

class Transform(beam.DoFn):
  # Use classes and functions to perform transformations on your PCollections
  # Yeld or return the element(s) needed as input for the next transform

  class split_line(beam.DoFn):

  def process(self,element):

    element [str(element)]
    print('I am inside split line function')
    # print(i)
    # element = str(element)
    element_list = element.split(sep=',')

    user = element_list[0]
    gender = element_list[1]
    age = element_list[2]
    address = element_list[3]
    date_joined = element_list[4]

    user_list.append(user)
    gender_list.append(gender)
    age_list.append(age)
    address_list.append(address)
    date_joined_list.append(date_joined)

    print(user_list)

    return user, gender, age, address, date_joined

  def process(self, element):

    # element = str(element)
    # element = element.replace(',', '~')
    # element = element.replace('/', '-')
    # print(element)
    # print('----------------')
    # element = [str(element)]

    return [str(element)]




class Printer(beam.DoFn):
  def process(self,data_item):
    print(data_item)

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

  # Read the input file into a PCollection & perform transformations
  output = (
      p
      | 'read' >> ReadFromText(known_args.input)
      # | 'transform' >> beam.ParDo(Transform())
      | 'split_line' >> beam.ParDo(split_line())
      # | 'Splitter using beam.Map' >> beam.Map(lambda record: (record.split(','))[0])
      # | 'Print the data' >> beam.ParDo(Printer())
      # | 'write' >> WriteToText(known_args.output)
      )

  result = p.run()
  print('after pipeline finished')
  result.wait_until_finish()


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
