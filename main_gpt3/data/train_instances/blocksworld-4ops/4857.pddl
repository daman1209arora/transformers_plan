

(define (problem BW-rand-6)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 )
(:init
(arm-empty)
(on-table b1)
(on b2 b1)
(on-table b3)
(on b4 b6)
(on-table b5)
(on b6 b5)
(clear b2)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b2)
(on b2 b6)
(on b4 b3)
(on b5 b4)
(on b6 b5))
)
)


