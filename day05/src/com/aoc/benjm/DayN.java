package com.aoc.benjm;

import java.util.*;
import java.util.stream.IntStream;

public class DayN {
    public long partOne(String filename) {
        return run(filename, false);
    }

    public long partTwo(String filename) {
        return run(filename, true);
    }

    private long run(String filename, boolean isPartTwo) {
        Scanner scanner = new Scanner(DayN.class.getResourceAsStream(filename));
        //TODO
        Map<String,Integer> counter = new HashMap<>();
        while (scanner.hasNextLine()) {
            String nextLine = scanner.nextLine();
            String[] line = nextLine.split(" -> ");
            String[] left = line[0].split(",");
            int lx = Integer.valueOf(left[0]);
            int ly = Integer.valueOf(left[1]);
            String[] right = line[1].split(",");
            int rx = Integer.valueOf(right[0]);
            int ry = Integer.valueOf(right[1]);
            int xmin = Math.min(lx,rx);
            int xmax = Math.max(lx,rx);
            int ymin = Math.min(ly,ry);
            int ymax = Math.max(ly,ry);
            if (ymin == ymax) {
                int y = ymin;
                for (int x = xmin; x <= xmax; x++) {
                    String id = x+","+y;
                    counter.put(id, counter.getOrDefault(id,0) + 1);
                }
            } else if (xmin == xmax) {
                int x = xmin;
                for (int y = ymin; y <= ymax; y++) {
                    String id = x+","+y;
                    counter.put(id, counter.getOrDefault(id,0) + 1);
                }
            } else if (isPartTwo) {
                int dx = rx>lx?1:-1;
                int dy = ry>ly?1:-1;
                for (int x = lx, y = ly; x <= xmax && x >= xmin && y <= ymax && y >= ymin;) {
                    String id = x+","+y;
                    counter.put(id, counter.getOrDefault(id,0) + 1);
                    x+=dx;
                    y+=dy;
                }
            }
        }

        long count = 0;
        for (int val : counter.values()) {
            if (val > 1) {
                count += 1;
            }
        }

        return count;
    }
}
class Util {

    public static void sysout(String s) {
        System.out.println(s);
    }
}