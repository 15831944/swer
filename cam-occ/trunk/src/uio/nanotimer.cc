// adapted from http://allmybrain.com/2008/06/10/timing-cc-code-on-linux/

/**************************************************************************
*   Copyright (C) 2010 by Mark Pictor                                     *
*   mpictor@gmail.com                                                     *
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
*   This program is distributed in the hope that it will be useful,       *
*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*   GNU General Public License for more details.                          *
*                                                                         *
*   You should have received a copy of the GNU General Public License     *
*   along with this program; if not, write to the                         *
*   Free Software Foundation, Inc.,                                       *
*   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
**************************************************************************/


#include <cstdio>
#include <QString>
#include "uio.hh"
#include "nanotimer.hh"

//clock_gettime requires librt
//CLOCK_MONOTONIC_RAW requires kernel 2.6.28 and libc6 >> 2.11.2
//with earlier kernels use CLOCK_MONOTONIC or CLOCK_REALTIME
#ifndef CLOCK_MONOTONIC_RAW
#define CLOCK_MONOTONIC_RAW CLOCK_MONOTONIC
#endif


void nanotimer::start() {
  clock_gettime(CLOCK_MONOTONIC_RAW, &begin);
}

long nanotimer::getElapsed(){
  timespec now,delta;
  clock_gettime(CLOCK_MONOTONIC_RAW, &now);
  delta.tv_sec = now.tv_sec - begin.tv_sec;
  delta.tv_nsec = now.tv_nsec - begin.tv_nsec;
  return delta.tv_sec*1000000000 + delta.tv_nsec;
}

double nanotimer::getElapsedS(){
  timespec now,delta;
  clock_gettime(CLOCK_MONOTONIC_RAW, &now);
  delta.tv_sec = now.tv_sec - begin.tv_sec;
  delta.tv_nsec = now.tv_nsec - begin.tv_nsec;
  return delta.tv_sec + delta.tv_nsec/1000000000.0;
}

QString nanotimer::humanreadable(double s) {
  QString out;// = "";
  if (s > 60) {
    int m;
    m = s/60;
    s = s-(double)(m*60);
    out = m /*uio::toString(m)*/ + QString("m, ");
  }
  if (s > .01) {
    out += s; /*uio::toString(s)*/ 
    out += "s";
  } else {
    out = s*1000000; /*uio::toString(s*1000000)*/ 
    out += "us";
  }
  return out;
}

/*
void timer::stopTimer( ) {
  gettimeofday(&(timer.stop),NULL);
  }
  */

/*double timer::getElapsedTime() {
  timeval res;
  timersub(&(timer.stop),&(timer.start),&res);
  return res.tv_sec + res.tv_usec/1000000.0; // 10^6 uSec per second
}*/

/* more accurate
!!! REQUIRES librt.so
timespec ts;
clock_gettime(CLOCK_REALTIME, &ts); // Works on Linux
CLOCK_MONOTONIC_RAW // kernel 2.6.28+
*/
