import { parse, parseFile, formatters } from "plantuml-parser";

import fs from "node:fs";

try {
  const file1 = fs.readFileSync("human-diagram.puml", "utf8");
  const file2 = fs.readFileSync("gpt-diagram.puml", "utf8");

  // parse PlantUML
  const elements1 = parse(file1);
  const elements2 = parse(file2);

  // Format and print parse result
  console.log(formatters.default(elements1));
  console.log(formatters.default(elements2));
  compareElements(elements1, elements2);
  console.log(elements1);
} catch (err) {
  console.error(err);
}

function compareElements(elements1, elements2) {
  // Assuming elements1 and elements2 are arrays of class definitions and relationships from two different sources.
  console.log("elems", elements1, elements2);
  elements1.forEach((elem1) => {
    const elem2 = elements2.find((e) => e.name === elem1.name);
    if (!elem2) {
      console.log(`Class '${elem1.name}' is missing in the second dataset.`);
      stats.major.fn += 1;
      return;
    }

    // Compare attributes and methods
    elem1.members.forEach((member) => {
      const counterpart = elem2.members.find((m) => m.name === member.name);
      if (!counterpart) {
        console.log(
          `Member '${member.name}' in class '${elem1.name}' is missing in the second dataset.`,
        );
        stats.minor.fn += 1;
      } else {
        // Compare member details
        if (
          member.accessor !== counterpart.accessor ||
          member.returnType !== counterpart.returnType ||
          member._arguments !== counterpart._arguments
        ) {
          console.log(
            `Discrepancy in member '${member.name}' of class '${elem1.name}': Expected ${JSON.stringify(member)} but found ${JSON.stringify(counterpart)}.`,
          );
          stats.minor.fp += 1;
        }
      }
    });

    // Compare relationships if the element represents a relationship
    if (elem1.hasOwnProperty("left") && elem1.hasOwnProperty("right")) {
      const rel2 = elements2.find(
        (e) => e.left === elem1.left && e.right === elem1.right,
      );
      if (!rel2) {
        console.log(
          `Relationship from '${elem1.left}' to '${elem1.right}' is missing in the second dataset.`,
        );
        stats.major.fn += 1;
      } else {
        // Compare relationship attributes
        [
          "leftType",
          "rightType",
          "leftArrowHead",
          "rightArrowHead",
          "leftArrowBody",
          "rightArrowBody",
          "leftCardinality",
          "rightCardinality",
          "label",
        ].forEach((attr) => {
          if (elem1[attr] !== rel2[attr]) {
            console.log(
              `Discrepancy in relationship attribute '${attr}' from '${elem1.left}' to '${elem1.right}': Expected '${elem1[attr]}' but found '${rel2[attr]}'.`,
            );
            stats.minor.fp += 1;
          }
        });
      }
    }
  });

  // Report elements in the second dataset not found in the first
  elements2.forEach((elem2) => {
    if (!elements1.find((e) => e.name === elem2.name)) {
      console.log(`Class '${elem2.name}' is extra in the second dataset.`);
      stats.major.fp += 1;
    }
  });
}

// Run comparison
printStats();
