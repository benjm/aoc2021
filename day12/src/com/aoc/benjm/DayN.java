package com.aoc.benjm;

import java.util.*;
import java.util.stream.Collectors;

public class DayN {
    public long partOne(String filename) {
        return run(filename, false);
    }

    public long partTwo(String filename) {
        return run(filename, true);
    }

    public static final String start = "start";
    public static final String end = "end";

    private long run(String filename, boolean isPartTwo) {
        Scanner scanner = new Scanner(DayN.class.getResourceAsStream(filename));
        Set<String> links = new HashSet<>();
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine();
            if (line.startsWith(start) || line.endsWith(end)) {
                links.add(line);
            } else {
                String[] lr = line.split("-");
                String l = lr[0];
                String r = lr[1];
                if (l.equals(start) || r.equals(end)) {
                    links.add(l+"-"+r);
                } else if (l.equals(end) || r.equals(start)) {
                    links.add(r+"-"+l);
                } else {
                    links.add(l + "-" + r);
                    links.add(r + "-" + l);
                }
            }
        }
        Set<String> paths = links.stream().filter(s -> s.startsWith(start)).collect(Collectors.toSet());
        Set<String> completed = new HashSet<>();
        while (paths.size() > 0) {
            Set<String> nextPaths = new HashSet<>();
            for (String path : paths) {
                String suffix = path.substring(path.length() - 3);
                if (suffix.equals(end)) {
                    completed.add(path);
                } else {
                    String last = suffix.substring(1);
                    Set<String> maybeOnwardPaths = links.stream().filter(s -> s.startsWith(last)).collect(Collectors.toSet());
                    Set<String> onwardPaths;
                    if (!isPartTwo) {
                        onwardPaths = maybeOnwardPaths.stream().filter(s ->
                                s.endsWith(end) ||
                                        Character.isUpperCase(s.charAt(3)) ||
                                        !path.contains("-" + s.substring(3) + "-")
                        ).collect(Collectors.toSet());
                    } else {
                        onwardPaths = maybeOnwardPaths.stream().filter(s ->
                                s.endsWith(end) ||
                                        Character.isUpperCase(s.charAt(3)) ||
                                        !doubleVisit(path) ||
                                        !path.contains(s.substring(3))
                        ).collect(Collectors.toSet());
                    }
                    for (String onwardPath : onwardPaths) {
                        nextPaths.add(path+onwardPath.substring(2));
                    }
                }
            }
            paths.clear();
            paths.addAll(nextPaths);
        }
//        sysout("COMPLETED: ");
//        for (String s : completed.stream().sorted().collect(Collectors.toList())) {
//            sysout(s);
//        }
        return completed.size();
    }

    private boolean doubleVisit(String path) {
        Set<String> caves = new HashSet<>();
        for (String cave : path.split("-")) {
            if (Character.isLowerCase(cave.charAt(0))) {
                if (caves.contains(cave)) return true;
                else caves.add(cave);
            }
        }
        return false;
    }

    private void sysout(String s) {
        System.out.println(s);
    }
}
