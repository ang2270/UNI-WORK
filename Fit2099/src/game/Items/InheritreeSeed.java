package game.Items;

import game.GroundEntity.Crop;
import game.GroundEntity.Inheritree;

/**
 * Subclass of SeedItem this represents a InheritreeSeed item
 * @author Angus Ashby
 */
public class InheritreeSeed extends SeedItem {
    public InheritreeSeed() {
        super("Inheritree Seed", '*', true, new Inheritree(), "Inheritree");
    }
    /**
     * Returns a new instance of the Plant this Seed Grows into when planted
     */
    @Override
    protected Crop newInstanceOfCrop() {
        return new Inheritree();
    }
}
