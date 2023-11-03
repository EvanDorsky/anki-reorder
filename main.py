#!/usr/bin/env python3

import os
import argparse
import pandas as pd

def countchars(txt, char):
  count = 0
  for c in txt:
    if c == char:
      count+=1

  return count

def ankilines(lines, n_fields):
  linenos = []
  for i, line in enumerate(lines):
    if countchars(line, "\t") > (n_fields-1):
      linenos += [i]

  return linenos

def create_out_path(path):
  path, ext = os.path.splitext(path)

  return path + "_reordered" + ext

def main(args):
  key_order_path = args.keys

  deck_path = args.deck

  out_path = create_out_path(deck_path)

  with open(deck_path) as f:
    deck_lines = f.readlines()

  key2deck = {}
  deck_idxs = []
  for i, line in enumerate(deck_lines):
    if line[0] != "#":
      key2deck[line.split('\t')[0].strip()] = i
      deck_idxs += [i]

  # if notes span multiple lines
  if args.n_fields > 0:
    deck_idxs = ankilines(deck_lines, args.n_fields)
    if not deck_idxs:
      print("Error: Failed to find notes in deck file.")
      print("Number of fields specified: %i" % args.n_fields)
      print("Try lowering the number of fields.")
      exit(1)


  out_keys_df = pd.read_csv(key_order_path, header=None)
  out_keys = list(out_keys_df[0])

  print("Searching for matching notes in deck. Notes: %i" % len(out_keys))
  count = 0
  new_idx2deck = {}
  # new_idx2deck maps a key's new idx to its idx in the deck
  for i, k in enumerate(out_keys):
    if k in key2deck:
      count+=1
      new_idx2deck[i] = key2deck[k]

  print("Matching notes: %i" % count)

  itemlinenos = []
  # for each out_keys_df idx...
  for key in new_idx2deck:
    # get all the deck_lines corresponding to the kd idx, put those in another dict
    itemstart = new_idx2deck[key]
    idx = deck_idxs.index(itemstart)
    itemend = deck_idxs[idx+1]-1
    itemlinenos += [[itemstart, itemend]]

  print("Adding %i items to new deck: %s" % (len(itemlinenos), out_path))

  newlines = deck_lines[:3]
  for linepair in itemlinenos:
    newlines += deck_lines[linepair[0]:linepair[1]+1]

  with open(out_path, "w") as f:
    for line in newlines:
      f.write(line)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('deck',
    help="Anki deck (.txt export) to be reordered")
  parser.add_argument('keys',
    help="CSV file with keys in desired order")
  parser.add_argument('-n', '--n-fields', type=int, default=-1,
    help="Approximate number of fields in note (only required for notes that span multiple lines in the deck file)")

  args = parser.parse_args()

  main(args)