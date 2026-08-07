package edu.monash.fit2099.demo.huntsman;

import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.positions.FancyGroundFactory;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.World;

import java.util.Arrays;
import java.util.List;

public class Application {

    public static void main(String[] args) {

        World world = new World(new Display());

        FancyGroundFactory groundFactory = new FancyGroundFactory(new Dirt());

        List<String> map = Arrays.asList(
                ".....",
                ".....",
                ".....",
                ".....",
                "....."
        );

        GameMap gameMap = new GameMap("Polymorphia", groundFactory, map);
        world.addGameMap(gameMap);

        gameMap.at(0, 0).addActor(new HuntsmanSpider());

        Player player = new Player("Intern", '@', 4);
        world.addPlayer(player, gameMap.at(2, 2));

        world.run();
    }

}
