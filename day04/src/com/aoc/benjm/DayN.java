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
        List<Integer> draw = readDraw(scanner);
        Util.sysout("draw: " + draw);
        int fastest = Integer.MAX_VALUE;
        int slowest = 0;
        long fastestScore = 0l;
        long slowestScore = 0l;
        while (scanner.hasNext()) {
            Board board = new Board(scanner);
            Optional<Integer> turn = board.eval(draw);
            if (fastest > turn.orElse(Integer.MAX_VALUE)) {
                fastest = turn.orElse(Integer.MAX_VALUE);
                fastestScore = board.getScore();
            }
            if (slowest < turn.orElse(0)) {
                slowest = turn.orElse(0);
                slowestScore = board.getScore();
            }
        }
        return isPartTwo ? slowestScore : fastestScore;
    }

    private List<Integer> readDraw(Scanner scanner) {
        return Util.readInts(scanner.nextLine(), ",");
    }
}
class Util {
    public static List<Integer> readInts(String nextLine, String splitBy) {
        String[] line = nextLine.split(splitBy);
        List<Integer> draw = new ArrayList<>(line.length + 1);
        if (line.length > 0) {
            for (String s : line) {
                if (s.length() > 0) { draw.add(Integer.valueOf(s)); }
            }
        }
        return draw;
    }

    public static void sysout(String s) {
        //System.out.println(s);
    }
}

class Board {
    List<Integer> numbers = new ArrayList<>();
    List<Integer> cols = new ArrayList<>();
    List<Integer> rows = new ArrayList<>();
    List<Integer> marked = new ArrayList<>();
    int turns = 0;

    public long getScore() {
        return score;
    }

    long score = 0l;

    public Board(Scanner scanner) {
        scanner.nextLine();
        for (int i = 0; i < 5; i++) {
            numbers.addAll(Util.readInts(scanner.nextLine(), " "));
        }
    }

    public Optional<Integer> eval(List<Integer> draw) {
        marked.clear();
        turns = 0;
        score = 0l;
        rows.clear();
        cols.clear();
        rows.addAll(List.of(0,0,0,0,0));
        cols.addAll(List.of(0,0,0,0,0));
        for (int i : draw) {
            turns+=1;
            if (numbers.contains(i)) {
                marked.add(i);
                int indexOfI = numbers.indexOf(i);
                int row = indexOfI / 5;
                int col = indexOfI % 5;
                rows.set(row, rows.get(row) + 1);
                cols.set(col, cols.get(col) + 1);
                if (rows.contains(5) || cols.contains(5)) {
                    int sumAll = numbers.stream().mapToInt(Integer::intValue).sum();
                    int sumMarked = marked.stream().mapToInt(Integer::intValue).sum();
                    int sumUnmarked = sumAll - sumMarked;
                    score = sumUnmarked * i;
                    Util.sysout("\nmarked: " + marked);
                    Util.sysout ("sum rest: " + sumUnmarked);
                    Util.sysout ("current: " + i);
                    Util.sysout ("score: " + score);
                    return Optional.of(turns);
                }
            }
        }
        return Optional.empty();
    }
}
