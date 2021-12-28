package com.aoc.benjm;

import java.util.*;

public class DayN {

    public long partOne(String filename) {
        return run(filename, false);
    }

    public long partTwo(String filename) {
        return run(filename, true);
    }

    private long run(String filename, boolean isPartTwo) {
        Scanner scanner = new Scanner(DayN.class.getResourceAsStream(filename));
        List<String> lines = new ArrayList<>();
        while (scanner.hasNextLine()) {
            lines.add(scanner.nextLine());
        }
        final int height = lines.size();
        final int width = lines.get(0).length();
        final Map<String, Space> spaces = new HashMap<>(height * width);
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                final Space space = new Space(y,x,lines.get(y).charAt(x), height, width);
                spaces.put(space.id, space);
            }
        }
        long turns = turnsUntilStationary(spaces);
        return turns;
    }

    private long turnsUntilStationary(Map<String, Space> spaces) {
        long count = moveEast(spaces) + moveSouth(spaces);
        long turns = count > 0 ? 1 : 0;
        while (count > 0) {
            turns++;
            count = moveEast(spaces) + moveSouth(spaces);
        }
        return turns;
    }

    private long moveEast(Map<String, Space> spaces) {
        Set<Space> willMove = new HashSet<>();
        for (Space space : spaces.values()) {
            if (space.getC() == Space.east && spaces.get(space.spaceEastId).getC() == Space.empty) {
                willMove.add(space);
            }
        }
        for (Space space : willMove) {
            space.setC(Space.empty);
            spaces.get(space.spaceEastId).setC(Space.east);
        }
        return willMove.size();
    }

    private long moveSouth(Map<String, Space> spaces) {
        Set<Space> willMove = new HashSet<>();
        for (Space space : spaces.values()) {
            if (space.getC() == Space.south && spaces.get(space.spaceSouthId).getC() == Space.empty) {
                willMove.add(space);
            }
        }
        for (Space space : willMove) {
            space.setC(Space.empty);
            spaces.get(space.spaceSouthId).setC(Space.south);
        }
        return willMove.size();
    }
}
