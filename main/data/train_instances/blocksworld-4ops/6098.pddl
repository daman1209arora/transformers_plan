

(define (problem BW-rand-6)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 )
(:init
(arm-empty)
(on-table b1)
(on b2 b6)
(on b3 b2)
(on b4 b5)
(on-table b5)
(on b6 b1)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b5)
(on b2 b4)
(on b6 b1))
)
)

