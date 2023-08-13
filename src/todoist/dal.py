#!/usr/bin/env python3

from pathlib import PurePath, Path
from typing import List, Dict, Union, Iterator, NamedTuple, Any, Sequence, Optional, Set
import json
from pathlib import Path
from datetime import datetime
import logging

import pytz

from .exporthelpers.dal_helper import PathIsh, Json, Res

def get_logger():
    return logging_helper.logger('todoist')

class DAL:
    ## TODO Allow selecting arbitrary dated file
    def __init__(self, sources: Sequence[PathIsh]) -> None:
        self.sources = [p if isinstance(p, Path) else Path(p) for p in sources]

    def raw(self):
        for f in sorted(self.sources):
            with f.open(encoding="utf-8") as fo:
                yield json.load(fo)

    def latest(self):
      latest_file = sorted(self.sources)[-1]

      with latest_file.open(encoding="utf-8") as fo:
          return json.load(fo)

    def projects(self) -> Iterator[Res[Json]]:
      latest_file = self.latest()
      yield latest_file['projects']

    def tasks(self, id: str) -> Iterator[Res[Json]]:
      latest_file = self.latest()
      yield latest_file['tasks']

    def completed(self, since: str, until: str, id: str) -> Iterator[Res[Json]]:
      latest_file = self.latest()
      for t in latest_file['tasks']:
        if t['completed']:
          yield t

    def activity(self, _id: str) -> Iterator[Res[Json]]:
      latest_file = self.latest()
      if _id:
        for t in latest_file['activity']['events']:
          if str(t['id']) == str(_id):
            yield t
      else:
        yield latest_file['activity']

    def taskComment(self, _id: str) -> Iterator[Res[Json]]:
      latest_file = self.latest()
      for t in latest_file['tasks']:
        if _id and str(t['id']) == str(_id):
          yield t['comments']
        elif not _id:
          yield t['comments']

if __name__ == '__main__':
    dal_helper.main(DAL=DAL)
